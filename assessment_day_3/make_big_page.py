from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

output_path = DATA_DIR / "large_attendance.html"

with output_path.open("w", encoding="utf-8") as file:
    file.write("<html><body>\n")
    file.write("<h1>Large Student Attendance Report</h1>\n")

    for student_id in range(1, 501):
        attended = 60 + (student_id % 41)

        file.write(
            f"<p>Student ID: {student_id}; "
            f"Days attended: {attended}; "
            f"Working days: 100; "
            f"Attendance: {attended} percent</p>\n"
        )

    file.write("</body></html>\n")

print("Large report created:", output_path)
print("Number of sample records:", 500)