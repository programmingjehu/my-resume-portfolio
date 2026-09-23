from pathlib import Path

cv_path = Path("cv.pdf")

sections = [
    "JEHU - CURRICULUM VITAE",
    "",
    "Email: jehucadiz3@gmail.com",
    "Phone: +63 9 07 456 9882",
    "Location: San Vicente Pamplona, Philippines",
    "",
    "OBJECTIVE",
    "Focused and motivated IT student with a passion for technology, programming, and web development.",
    "Eager to learn new skills, build practical projects, and contribute to meaningful digital solutions.",
    "",
    "SKILLS",
    "- HTML",
    "- CSS",
    "- JavaScript",
    "- C#",
    "- Web Development",
    "- UI/UX Design",
    "- Programming",
    "- Problem Solving",
    "- Responsive Design",
    "- Teamwork and Communication",
    "",
    "EDUCATION",
    "- Information Technology, STI College Naga City (2023 - Present)",
    "- Senior High School, STI College Naga City (2021 - 2023)",
    "",
    "PROJECTS",
    "- Portfolio Website",
    "- Task Manager App",
    "- School Website",
    "",
    "EXPERIENCE",
    "- Freelance Web Developer (2024 - Present)",
    "  Creating personal and client-oriented web projects and improving technical skills.",
]

content_lines = []
for line in sections:
    if line == "":
        content_lines.append("")
    else:
        content_lines.append(line)

stream_text = "BT\n/F1 12 Tf\n72 760 Td\n"
y = 760
for line in sections:
    if line == "":
        y -= 18
        continue
    escaped = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
    if line in {"JEHU - CURRICULUM VITAE", "OBJECTIVE", "SKILLS", "EDUCATION", "PROJECTS", "EXPERIENCE"}:
        stream_text += "/F1 14 Tf\n"
    else:
        stream_text += "/F1 12 Tf\n"
    stream_text += f"72 {y} Td\n({escaped}) Tj\n"
    y -= 18
stream_text += "ET\n"

stream = stream_text.encode("latin-1", "replace")
objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1") + stream + b"\nendstream",
]

pdf = bytearray(b"%PDF-1.4\n")
offsets = [0]
for i, obj in enumerate(objects, start=1):
    offsets.append(len(pdf))
    pdf.extend(f"{i} 0 obj\n".encode("latin-1"))
    pdf.extend(obj)
    pdf.extend(b"\nendobj\n")

xref_pos = len(pdf)
pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
pdf.extend(b"0000000000 65535 f \n")
for off in offsets[1:]:
    pdf.extend(f"{off:010d} 00000 n \n".encode("latin-1"))
pdf.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("latin-1"))

cv_path.write_bytes(pdf)
print(f"Created {cv_path} ({cv_path.stat().st_size} bytes)")
