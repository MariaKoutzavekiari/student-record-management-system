# =============================================================================
# Student Record Management System
# Fixed version of the original top-down program
# =============================================================================

import csv

student_records = []
csv_filename = ""
menu_choice = ""
csv_loaded = False

search_id = ""
found_student = None
search_index = 0

row_number = 0
current_student = None

student_id = ""
student_name = ""
major = ""
gpa = ""
total_credits = ""

print("=" * 60)
print("   Student Record Management System")
print("=" * 60)

while True:
    print()
    print("Please select an option:")
    print("  1. Read CSV")
    print("  2. List CSV Contents")
    print("  3. Search for Student by ID")
    print("  4. Exit")
    print()

    menu_choice = input("Enter your choice (1-4): ").strip()

    if menu_choice == "1":
        csv_filename = input(
            "Enter the CSV filename (e.g., students.csv): "
        ).strip()

        # Reloading replaces the existing records instead of duplicating them.
        student_records.clear()

        try:
            with open(csv_filename, newline="", encoding="utf-8") as csv_file:
                csv_reader = csv.DictReader(csv_file)

                for row in csv_reader:
                    student_id = row["StudentID"]
                    student_name = row["StudentName"]
                    major = row["Major"]
                    gpa = row["GPA"]
                    total_credits = row["TotalCredits"]

                    student_record = {
                        "StudentID": student_id,
                        "StudentName": student_name,
                        "Major": major,
                        "GPA": gpa,
                        "TotalCredits": total_credits,
                    }

                    student_records.append(student_record)

            csv_loaded = True
            print()
            print(
                f"Success! {len(student_records)} student record(s) "
                f"loaded from '{csv_filename}'."
            )

        except FileNotFoundError:
            csv_loaded = False
            print()
            print(f"File '{csv_filename}' was not found.")

    elif menu_choice == "2":
        if not csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")
        else:
            print()
            print("-" * 80)
            print(
                f"{'#':<5} {'Student ID':<12} {'Student Name':<22} "
                f"{'Major':<24} {'GPA':<6} {'Credits'}"
            )
            print("-" * 82)

            row_number = 1

            for current_student in student_records:
                print(
                    f"{row_number:<5}"
                    f"{current_student['StudentID']:<12}"
                    f"{current_student['StudentName']:<22}"
                    f"{current_student['Major']:<24}"
                    f"{current_student['GPA']:<6}"
                    f"{current_student['TotalCredits']}"
                )
                row_number += 1

            print("-" * 82)
            print(f"Total records: {len(student_records)}")

    elif menu_choice == "3":
        if not csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")
        else:
            search_id = input(
                "Enter the Student ID to search for: "
            ).strip().upper()

            # Reset the previous search result before every new search.
            found_student = None
            search_index = 0

            while search_index < len(student_records):
                if (
                    student_records[search_index]["StudentID"].upper()
                    == search_id
                ):
                    found_student = student_records[search_index]
                    break

                search_index += 1

            print()

            if found_student is None:
                print(f"No student found with ID '{search_id}'.")
            else:
                print("Student found!")
                print("-" * 40)
                print(f"  Student ID    : {found_student['StudentID']}")
                print(f"  Student Name  : {found_student['StudentName']}")
                print(f"  Major         : {found_student['Major']}")
                print(f"  GPA           : {found_student['GPA']}")
                print(f"  Total Credits : {found_student['TotalCredits']}")
                print("-" * 40)

    elif menu_choice == "4":
        print()
        print(
            "Thank you for using the Student Record Management System. "
            "Goodbye!"
        )
        break

    else:
        print()
        print(
            f"'{menu_choice}' is not a valid option. "
            "Please enter 1, 2, 3, or 4."
        )
