import csv
from pathlib import Path

DATA_FILE = Path("data/students.csv")
FIELDS = ["id", "name", "age", "course", "marks", "email"]

def setup():
    DATA_FILE.parent.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()

def load_students():
    setup()
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_students(students):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(students)

def valid_int(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            if maximum is not None and value > maximum:
                raise ValueError
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def valid_float(prompt, minimum=0, maximum=100):
    while True:
        try:
            value = float(input(prompt))
            if not minimum <= value <= maximum:
                raise ValueError
            return value
        except ValueError:
            print(f"Enter a number between {minimum} and {maximum}.")

def add_student():
    students = load_students()
    sid = input("Student ID: ").strip()
    if any(s["id"] == sid for s in students):
        print("Student ID already exists.")
        return
    name = input("Name: ").strip()
    age = valid_int("Age: ", 1, 100)
    course = input("Course: ").strip()
    marks = valid_float("Marks (0-100): ")
    email = input("Email: ").strip()
    students.append({"id": sid, "name": name, "age": str(age),
                     "course": course, "marks": str(marks), "email": email})
    save_students(students)
    print("Student added successfully.")

def update_student():
    students = load_students()
    sid = input("Enter Student ID to update: ").strip()
    for s in students:
        if s["id"] == sid:
            print("Press Enter to keep the existing value.")
            name = input(f"Name [{s['name']}]: ").strip() or s["name"]
            age_raw = input(f"Age [{s['age']}]: ").strip()
            course = input(f"Course [{s['course']}]: ").strip() or s["course"]
            marks_raw = input(f"Marks [{s['marks']}]: ").strip()
            email = input(f"Email [{s['email']}]: ").strip() or s["email"]
            s["name"] = name
            s["age"] = str(valid_int("New age: ", 1, 100)) if age_raw else s["age"]
            s["course"] = course
            s["marks"] = str(valid_float("New marks: ")) if marks_raw else s["marks"]
            s["email"] = email
            save_students(students)
            print("Student updated successfully.")
            return
    print("Student not found.")

def delete_student():
    students = load_students()
    sid = input("Enter Student ID to delete: ").strip()
    new_students = [s for s in students if s["id"] != sid]
    if len(new_students) == len(students):
        print("Student not found.")
    else:
        save_students(new_students)
        print("Student deleted successfully.")

def search_student():
    students = load_students()
    key = input("Enter Student ID or name: ").strip().lower()
    matches = [s for s in students if key in s["id"].lower() or key in s["name"].lower()]
    display(matches)

def display(students):
    if not students:
        print("No records found.")
        return
    print("-" * 95)
    print(f"{'ID':<10}{'Name':<22}{'Age':<7}{'Course':<18}{'Marks':<10}{'Email'}")
    print("-" * 95)
    for s in students:
        print(f"{s['id']:<10}{s['name']:<22}{s['age']:<7}{s['course']:<18}{s['marks']:<10}{s['email']}")
    print("-" * 95)

def report():
    students = load_students()
    if not students:
        print("No records available.")
        return
    students = sorted(students, key=lambda s: float(s["marks"]), reverse=True)
    display(students)
    avg = sum(float(s["marks"]) for s in students) / len(students)
    passed = sum(float(s["marks"]) >= 40 for s in students)
    print(f"Average marks: {avg:.2f}")
    print(f"Passed: {passed}/{len(students)}")

def main():
    setup()
    while True:
        print("\n=== STUDENT RECORD MANAGEMENT SYSTEM ===")
        print("1. Add student")
        print("2. Update student")
        print("3. Delete student")
        print("4. Search student")
        print("5. View all students")
        print("6. Performance report")
        print("7. Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1": add_student()
            elif choice == "2": update_student()
            elif choice == "3": delete_student()
            elif choice == "4": search_student()
            elif choice == "5": display(load_students())
            elif choice == "6": report()
            elif choice == "7":
                print("Thank you.")
                break
            else: print("Invalid choice.")
        except Exception as e:
            print(f"Operation failed: {e}")

if __name__ == "__main__":
    main()
