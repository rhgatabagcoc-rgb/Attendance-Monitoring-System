from datetime import datetime
import textwrap

# ============================================================
# ATTENDANCE MONITORING SYSTEM
# Python Console/Terminal Application
# Note: Data resets when the program closes.
# ============================================================

classes = []
students = []
attendance_records = []

# Class:      [class_id, section, subject, schedule, room]
# Student:    [student_id, name, age, class_id]
# Attendance: [student_id, class_id, date, status]


# ============================================================
# UNIVERSAL TABLE FUNCTION
# This function keeps ALL tables aligned.
# Long text wraps inside its column.
# ============================================================

def print_table(headers, rows, widths):
    # Calculate the total width of the table.
    total_width = sum(widths) + (3 * (len(widths) - 1))
    border = "-" * total_width

    def wrap_text(value, width):
        # Convert the value to text and wrap it if it is too long.
        return textwrap.wrap(
            str(value),
            width=width,
            break_long_words=True,
            break_on_hyphens=False
        ) or [""]

    def print_row(values):
        # Wrap every cell using its assigned column width.
        wrapped = [
            wrap_text(values[i], widths[i])
            for i in range(len(widths))
        ]

        # Find the number of lines needed by the tallest cell.
        max_lines = max(len(cell) for cell in wrapped)

        # Print each line using the same column positions.
        for line_number in range(max_lines):
            cells = []

            for i, cell in enumerate(wrapped):
                value = (
                    cell[line_number]
                    if line_number < len(cell)
                    else ""
                )
                cells.append(value.ljust(widths[i]))

            print(" | ".join(cells))

    # Display the table headings.
    print(border)
    print_row(headers)
    print(border)

    # Display the table contents.
    if not rows:
        print("No records found.")
    else:
        for row in rows:
            print_row(row)
            print(border)

    print()


# ============================================================
# GENERAL FUNCTIONS
# ============================================================

def pause():
    # Wait for the user before returning to the menu.
    input("\nPress Enter to continue...")


def get_date():
    # Ask for a date and validate its format.
    while True:
        date_text = input("Enter date (DD/MM/YYYY): ").strip()

        try:
            date_value = datetime.strptime(date_text, "%d/%m/%Y")
            return date_value.strftime("%d/%m/%Y")

        except ValueError:
            print("Invalid date. Please use DD/MM/YYYY.")


def find_class(class_id):
    # Find a class using its class ID.
    for class_info in classes:
        if class_info[0] == class_id:
            return class_info

    return None


def students_in_class(class_id):
    # Return all students registered in a specific class.
    return [
        student for student in students
        if student[3] == class_id
    ]


def print_class_table(class_list=None):
    # Display all classes using the universal table function.
    if class_list is None:
        class_list = classes

    rows = []

    for number, item in enumerate(class_list, start=1):
        rows.append([
            number,
            item[1],
            item[2],
            item[3],
            item[4]
        ])

    print("\nSECTION / CLASS LIST")

    print_table(
        ["No.", "Section", "Subject/Class", "Schedule", "Room"],
        rows,
        [5, 15, 20, 28, 15]
    )


def choose_class():
    # Let the user select a class from the class list.
    if not classes:
        print("\nNo sections/classes found. Add a class first.")
        return None

    print_class_table()

    while True:
        choice = input(
            "Choose class number (0 to cancel): "
        ).strip()

        if choice == "0":
            return None

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(classes):
                return classes[number - 1]

        print("Invalid choice. Please select a number from the table.")


def print_student_table(student_list=None):
    # Display student information using aligned columns.
    if student_list is None:
        student_list = students

    rows = []

    for student in student_list:
        class_info = find_class(student[3])

        if class_info:
            rows.append([
                student[0],
                student[1],
                student[2],
                class_info[1],
                class_info[2],
                class_info[3],
                class_info[4]
            ])

    print("\nSTUDENT INFORMATION")

    print_table(
        [
            "Student ID",
            "Student Name",
            "Age",
            "Section",
            "Subject/Class",
            "Schedule",
            "Room"
        ],
        rows,
        [16, 22, 5, 12, 20, 25, 15]
    )


# ============================================================
# SECTION AND STUDENT MANAGEMENT
# ============================================================

def add_section():
    # Create a new section/class.
    while True:
        print("\n========== ADD SECTION / CLASS ==========")

        section = input("Enter section name: ").strip()
        subject = input("Enter subject/class: ").strip()
        schedule = input("Enter schedule: ").strip()
        room = input("Enter room: ").strip()

        # Make sure all class details are entered.
        if not section or not subject or not schedule or not room:
            print("All fields are required.")
            continue

        # Generate a new class ID.
        class_id = max(
            [item[0] for item in classes],
            default=0
        ) + 1

        # Save the class information.
        classes.append([
            class_id,
            section,
            subject,
            schedule,
            room
        ])

        print("\nSection/class added successfully!")
        print_class_table()

        answer = input(
            "Add students to this class? (yes/no): "
        ).strip().lower()

        if answer in ("yes", "y"):
            add_student_to_class(class_id)

        answer = input(
            "\nAdd another section/class? (yes/no): "
        ).strip().lower()

        if answer not in ("yes", "y"):
            break


def add_student_to_class(class_id):
    # Add students to the selected class.
    class_info = find_class(class_id)

    if class_info is None:
        print("Class not found.")
        return

    while True:
        print(
            f"\nAdding student to {class_info[1]} "
            f"- {class_info[2]}"
        )

        student_id = input("Enter Student ID: ").strip()

        if not student_id:
            print("Student ID cannot be empty.")
            continue

        # Prevent duplicate IDs within the same class.
        duplicate = any(
            student[0].lower() == student_id.lower()
            and student[3] == class_id
            for student in students
        )

        if duplicate:
            print("This student is already registered in this class!")
            continue

        name = input("Enter student name: ").strip()
        age_text = input("Enter student age: ").strip()

        if not name or not age_text:
            print("Name and age are required.")
            continue

        # Check whether the age is a valid positive number.
        if not age_text.isdigit() or int(age_text) <= 0:
            print("Age must be a positive number.")
            continue

        # Save the student's information.
        students.append([
            student_id,
            name,
            int(age_text),
            class_id
        ])

        print("\nStudent added successfully!")
        print_student_table()

        answer = input(
            "Add another student to this class? (yes/no): "
        ).strip().lower()

        if answer not in ("yes", "y"):
            break


def add_student_menu():
    # Display student-management options.
    while True:
        print("\n========== STUDENT MANAGEMENT ==========")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            class_info = choose_class()

            if class_info:
                add_student_to_class(class_info[0])

        elif choice == "2":
            print_student_table()
            pause()

        elif choice == "3":
            search_student()

        elif choice == "4":
            delete_student()

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


def search_student():
    # Search for a student using their Student ID.
    student_id = input(
        "\nEnter Student ID to search: "
    ).strip()

    found = [
        student for student in students
        if student[0].lower() == student_id.lower()
    ]

    if found:
        print_student_table(found)
    else:
        print("Student not found.")

    pause()


def delete_student():
    # Delete a student's enrollment and related attendance records.
    student_id = input(
        "\nEnter Student ID to delete: "
    ).strip()

    found = [
        student for student in students
        if student[0].lower() == student_id.lower()
    ]

    if not found:
        print("Student not found.")
        pause()
        return

    print_student_table(found)

    confirm = input(
        "Delete these enrollment(s) and attendance records? (yes/no): "
    ).strip().lower()

    if confirm in ("yes", "y"):
        class_ids = {
            student[3] for student in found
        }

        # Remove the student's enrollment.
        students[:] = [
            student for student in students
            if not (
                student[0].lower() == student_id.lower()
                and student[3] in class_ids
            )
        ]

        # Remove attendance records connected to those enrollments.
        attendance_records[:] = [
            record for record in attendance_records
            if not (
                record[0].lower() == student_id.lower()
                and record[1] in class_ids
            )
        ]

        print("Student and related attendance records deleted.")

    else:
        print("Deletion cancelled.")

    pause()


# ============================================================
# ATTENDANCE FUNCTIONS
# ============================================================

def get_attendance_record(student_id, class_id, date):
    # Find a student's attendance for a particular date and class.
    for record in attendance_records:
        if (
            record[0].lower() == student_id.lower()
            and record[1] == class_id
            and record[2] == date
        ):
            return record

    return None


def record_attendance():
    # Record attendance for a selected class and date.
    print("\n========== RECORD ATTENDANCE ==========")

    class_info = choose_class()

    if not class_info:
        return

    class_id = class_info[0]
    class_students = students_in_class(class_id)

    if not class_students:
        print("No students are registered in this class.")
        pause()
        return

    date = get_date()

    print(f"\nSection: {class_info[1]}")
    print(f"Subject: {class_info[2]}")
    print(f"Schedule: {class_info[3]}")
    print(f"Room: {class_info[4]}")
    print(f"Date: {date}")

    print("\nAll students will be marked PRESENT by default.")
    print("Enter IDs of ABSENT students first.")
    print("Then enter IDs of LATE students.")
    print("Press Enter without an ID when finished.")

    # Create default Present records where no record exists.
    for student in class_students:
        record = get_attendance_record(
            student[0],
            class_id,
            date
        )

        if record is None:
            attendance_records.append([
                student[0],
                class_id,
                date,
                "Present"
            ])

    # Record students who are absent.
    while True:
        student_id = input(
            "\nEnter ID of ABSENT student (Enter to finish): "
        ).strip()

        if not student_id:
            break

        student = next(
            (
                s for s in class_students
                if s[0].lower() == student_id.lower()
            ),
            None
        )

        if student is None:
            print("Student ID not found in this class.")
            continue

        record = get_attendance_record(
            student[0],
            class_id,
            date
        )

        if record:
            record[3] = "Absent"
            print(f"{student[1]} marked Absent.")

    # Record students who are late.
    while True:
        student_id = input(
            "\nEnter ID of LATE student (Enter to finish): "
        ).strip()

        if not student_id:
            break

        student = next(
            (
                s for s in class_students
                if s[0].lower() == student_id.lower()
            ),
            None
        )

        if student is None:
            print("Student ID not found in this class.")
            continue

        record = get_attendance_record(
            student[0],
            class_id,
            date
        )

        if record:
            record[3] = "Late"
            print(f"{student[1]} marked Late.")

    print("\nAttendance saved successfully!")
    show_class_attendance(class_info, date)
    pause()


def show_class_attendance(class_info, date=None):
    # Display attendance records for a class.
    class_id = class_info[0]

    records = [
        record for record in attendance_records
        if record[1] == class_id
        and (date is None or record[2] == date)
    ]

    rows = []

    for record in records:
        student = next(
            (
                s for s in students
                if s[0].lower() == record[0].lower()
                and s[3] == class_id
            ),
            None
        )

        name = student[1] if student else "Unknown"

        rows.append([
            record[2],
            record[0],
            name,
            record[3]
        ])

    print("\nCLASS ATTENDANCE")

    print_table(
        ["Date", "Student ID", "Student Name", "Status"],
        rows,
        [14, 18, 28, 12]
    )


def print_attendance_records(records):
    # Display selected attendance records in aligned columns.
    rows = []

    for record in records:
        student = next(
            (
                s for s in students
                if s[0].lower() == record[0].lower()
                and s[3] == record[1]
            ),
            None
        )

        class_info = find_class(record[1])

        name = student[1] if student else "Unknown"
        section = class_info[1] if class_info else "Unknown"
        subject = class_info[2] if class_info else "Unknown"

        rows.append([
            record[2],
            record[0],
            name,
            section,
            subject,
            record[3]
        ])

    print("\nATTENDANCE RECORDS")

    print_table(
        [
            "Date",
            "Student ID",
            "Student Name",
            "Section",
            "Subject/Class",
            "Status"
        ],
        rows,
        [14, 18, 25, 15, 20, 12]
    )


def print_status_totals(records):
    # Count Present, Absent, and Late attendance records.
    present = sum(
        1 for record in records
        if record[3] == "Present"
    )

    absent = sum(
        1 for record in records
        if record[3] == "Absent"
    )

    late = sum(
        1 for record in records
        if record[3] == "Late"
    )

    # Display the totals in an aligned table.
    print("\nATTENDANCE TOTALS")

    print_table(
        ["Present", "Absent", "Late"],
        [[present, absent, late]],
        [15, 15, 15]
    )


def view_attendance():
    # Let the user view attendance by class, student, or date.
    while True:
        print("\n========== VIEW ATTENDANCE ==========")
        print("1. View by Section/Class")
        print("2. View by Student")
        print("3. View by Specific Date")
        print("0. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            class_info = choose_class()

            if not class_info:
                continue

            print("\n1. View all records")
            print("2. View by month")
            print("3. View by specific date")

            sub_choice = input("Choose an option: ").strip()

            records = [
                r for r in attendance_records
                if r[1] == class_info[0]
            ]

            if sub_choice == "2":
                month_text = input(
                    "Enter month and year (MM/YYYY): "
                ).strip()

                try:
                    datetime.strptime(month_text, "%m/%Y")

                    records = [
                        r for r in records
                        if datetime.strptime(
                            r[2], "%d/%m/%Y"
                        ).strftime("%m/%Y") == month_text
                    ]

                except ValueError:
                    print("Invalid month. Use MM/YYYY.")
                    pause()
                    continue

            elif sub_choice == "3":
                selected_date = get_date()

                records = [
                    r for r in records
                    if r[2] == selected_date
                ]

            elif sub_choice != "1":
                print("Invalid choice.")
                continue

            print_attendance_records(records)
            print_status_totals(records)
            pause()

        elif choice == "2":
            student_id = input("Enter Student ID: ").strip()

            records = [
                r for r in attendance_records
                if r[0].lower() == student_id.lower()
            ]

            print_attendance_records(records)
            print_status_totals(records)
            pause()

        elif choice == "3":
            selected_date = get_date()

            records = [
                r for r in attendance_records
                if r[2] == selected_date
            ]

            print_attendance_records(records)
            print_status_totals(records)
            pause()

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


def update_attendance():
    # Update an existing attendance record.
    print("\n========== UPDATE ATTENDANCE ==========")

    class_info = choose_class()

    if not class_info:
        return

    date = get_date()
    student_id = input("Enter Student ID: ").strip()

    record = get_attendance_record(
        student_id,
        class_info[0],
        date
    )

    if record is None:
        print("Attendance record not found.")
        pause()
        return

    print(f"Current status: {record[3]}")
    print("1. Present")
    print("2. Absent")
    print("3. Late")

    choice = input("Choose new status: ").strip()

    status_options = {
        "1": "Present",
        "2": "Absent",
        "3": "Late"
    }

    if choice in status_options:
        record[3] = status_options[choice]
        print("Attendance updated successfully.")

    else:
        print("Invalid choice. No changes made.")

    pause()


def attendance_summary():
    # Display attendance totals for each student in a class.
    class_info = choose_class()

    if not class_info:
        return

    class_id = class_info[0]
    rows = []

    for student in students_in_class(class_id):
        records = [
            r for r in attendance_records
            if r[0].lower() == student[0].lower()
            and r[1] == class_id
        ]

        present = sum(
            1 for r in records if r[3] == "Present"
        )

        absent = sum(
            1 for r in records if r[3] == "Absent"
        )

        late = sum(
            1 for r in records if r[3] == "Late"
        )

        rows.append([
            student[0],
            student[1],
            present,
            absent,
            late
        ])

    print(
        f"\nATTENDANCE SUMMARY - "
        f"{class_info[1]} / {class_info[2]}"
    )

    print_table(
        [
            "Student ID",
            "Student Name",
            "Present",
            "Absent",
            "Late"
        ],
        rows,
        [18, 28, 12, 12, 12]
    )

    pause()


# ============================================================
# MENUS
# ============================================================

def attendance_menu():
    # Display attendance options.
    while True:
        print("\n========== ATTENDANCE ==========")
        print("1. Record Attendance")
        print("2. View Attendance")
        print("3. Update Attendance")
        print("4. Attendance Summary by Section")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            record_attendance()

        elif choice == "2":
            view_attendance()

        elif choice == "3":
            update_attendance()

        elif choice == "4":
            attendance_summary()

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


def main():
    # Display the main menu and run the selected function.
    while True:
        print("\n========================================")
        print("       ATTENDANCE MONITORING SYSTEM")
        print("========================================")
        print("1. Add Section")
        print("2. Student Management")
        print("3. Attendance")
        print("0. Exit")
        print("========================================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_section()

        elif choice == "2":
            add_student_menu()

        elif choice == "3":
            attendance_menu()

        elif choice == "0":
            print("\nThank you for using the Attendance Monitoring System!")
            print("Program ended.")
            break

        else:
            print("Invalid choice. Please try again.")


# Start the program.
if __name__ == "__main__":
    main()