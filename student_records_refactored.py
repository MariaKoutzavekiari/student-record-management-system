# =============================================================================
# Student Record Management System
# Object-oriented refactored version
# =============================================================================

import csv


class Student:
    """Represent one student record."""

    def __init__(
        self,
        student_id,
        student_name,
        major,
        gpa,
        total_credits,
    ):
        """Initialize a student record."""
        self.student_id = student_id.strip().upper()
        self.student_name = student_name.strip()
        self.major = major.strip()
        self.gpa = float(gpa)
        self.total_credits = int(total_credits)

    def __str__(self):
        """Return the student in the original formatted display style."""
        return (
            f"  Student ID    : {self.student_id}\n"
            f"  Student Name  : {self.student_name}\n"
            f"  Major         : {self.major}\n"
            f"  GPA           : {self.gpa:g}\n"
            f"  Total Credits : {self.total_credits}"
        )


class GraduateStudent(Student):
    """Represent a graduate student with a thesis topic."""

    def __init__(
        self,
        student_id,
        student_name,
        major,
        gpa,
        total_credits,
        thesis_topic,
    ):
        """Initialize a graduate student record."""
        super().__init__(
            student_id,
            student_name,
            major,
            gpa,
            total_credits,
        )
        self.thesis_topic = thesis_topic.strip()

    def __str__(self):
        """Return the graduate student including the thesis topic."""
        return f"{super().__str__()}\n  Thesis Topic  : {self.thesis_topic}"


class StudentRoster:
    """Manage a collection of students loaded from a CSV file."""

    def __init__(self):
        """Initialize an empty student roster."""
        self.students = []
        self.csv_loaded = False
        self.filename = ""

    def load_csv(self, filename):
        """Load student records from a CSV file."""
        filename = filename.strip()
        new_students = []

        try:
            with open(filename, newline="", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)

                for row_number, row in enumerate(reader, start=2):
                    try:
                        student = Student(
                            row["StudentID"],
                            row["StudentName"],
                            row["Major"],
                            row["GPA"],
                            row["TotalCredits"],
                        )
                        new_students.append(student)
                    except (KeyError, TypeError, ValueError) as error:
                        print(
                            f"Error reading CSV row {row_number}: {error}. "
                            "Row skipped."
                        )

        except FileNotFoundError:
            print()
            print(f"File '{filename}' was not found.")
            return False
        except OSError as error:
            print()
            print(f"Unable to read '{filename}': {error}")
            return False

        # Replace the old list so loading the file twice does not create duplicates.
        self.students = new_students

        # Binary search requires the list to be sorted by the search key.
        self.students.sort(key=lambda student: student.student_id)

        self.filename = filename
        self.csv_loaded = True

        print()
        print(
            f"Success! {len(self.students)} student record(s) "
            f"loaded from '{filename}'."
        )
        return True

    def list_students(self):
        """Display every student in a formatted table."""
        if not self.csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")
            return

        print()
        print("-" * 80)
        print(
            f"{'#':<5} {'Student ID':<12} {'Student Name':<22} "
            f"{'Major':<24} {'GPA':<6} {'Credits'}"
        )
        print("-" * 82)

        for row_number, student in enumerate(self.students, start=1):
            print(
                f"{row_number:<5}"
                f"{student.student_id:<12}"
                f"{student.student_name:<22}"
                f"{student.major:<24}"
                f"{student.gpa:<6g}"
                f"{student.total_credits}"
            )

        print("-" * 82)
        print(f"Total records: {len(self.students)}")

    def search_by_id(self, search_id):
        """Find and display a student by ID using binary search."""
        if not self.csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")
            return None

        target_id = search_id.strip().upper()
        low = 0
        high = len(self.students) - 1

        while low <= high:
            middle = (low + high) // 2
            middle_student = self.students[middle]
            middle_id = middle_student.student_id

            if middle_id == target_id:
                print()
                print("Student found!")
                print("-" * 40)
                print(middle_student)
                print("-" * 40)
                return middle_student

            # Discard the half that cannot contain the target.
            if middle_id < target_id:
                low = middle + 1
            else:
                high = middle - 1

        print()
        print(f"No student found with ID '{target_id}'.")
        return None

    def run(self):
        """Run the menu-driven student record program."""
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
                filename = input(
                    "Enter the CSV filename (e.g., students.csv): "
                ).strip()
                self.load_csv(filename)

            elif menu_choice == "2":
                self.list_students()

            elif menu_choice == "3":
                if not self.csv_loaded:
                    print()
                    print(
                        "No data loaded. Please use Option 1 "
                        "to read a CSV file first."
                    )
                else:
                    search_id = input(
                        "Enter the Student ID to search for: "
                    ).strip()
                    self.search_by_id(search_id)

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


if __name__ == "__main__":
    roster = StudentRoster()
    roster.run()