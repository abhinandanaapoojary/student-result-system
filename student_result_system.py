# ─────────────────────────────────────────────
#  Student Result Management System
#  Author: Abhinandana A Poojary
#  Tech Stack: Python + MySQL
# ─────────────────────────────────────────────

import mysql.connector
from mysql.connector import Error

# ── Database Connection ───────────────────────
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",   # <-- change this
        database="student_results"
    )


# ── Setup ─────────────────────────────────────
def setup_database():
    conn = mysql.connector.connect(host="localhost", user="root", password="your_password")
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS student_results")
    cursor.execute("USE student_results")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            name        VARCHAR(100) NOT NULL,
            roll_number VARCHAR(20)  UNIQUE NOT NULL,
            department  VARCHAR(100)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            student_id  INT NOT NULL,
            subject     VARCHAR(100) NOT NULL,
            marks       FLOAT NOT NULL,
            max_marks   FLOAT NOT NULL DEFAULT 100,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database setup complete.")


# ── Grade Logic ───────────────────────────────
def compute_grade(marks, max_marks=100):
    pct = (marks / max_marks) * 100
    if pct >= 90: return "A+"
    if pct >= 80: return "A"
    if pct >= 70: return "B"
    if pct >= 60: return "C"
    if pct >= 50: return "D"
    return "F"


# ── Student Operations ────────────────────────
def add_student():
    name    = input("Student Name: ").strip()
    roll    = input("Roll Number: ").strip()
    dept    = input("Department: ").strip()
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, roll_number, department) VALUES (%s, %s, %s)",
            (name, roll, dept)
        )
        conn.commit()
        print(f"Student '{name}' added (ID: {cursor.lastrowid}).")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close(); conn.close()


def view_students():
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, roll_number, department FROM students ORDER BY id")
        rows = cursor.fetchall()
        if not rows:
            print("No students found."); return
        print(f"\n{'ID':<5} {'Name':<25} {'Roll No':<15} Department")
        print("─" * 60)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close(); conn.close()


def delete_student():
    view_students()
    try:
        sid    = int(input("\nEnter Student ID to delete: "))
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=%s", (sid,))
        conn.commit()
        print("Student deleted." if cursor.rowcount else "ID not found.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close(); conn.close()


# ── Result Operations ─────────────────────────
def add_result():
    view_students()
    try:
        sid     = int(input("\nEnter Student ID: "))
        subject = input("Subject: ").strip()
        marks   = float(input("Marks obtained: "))
        max_m   = float(input("Max marks (default 100): ") or 100)
        conn    = get_connection()
        cursor  = conn.cursor()
        cursor.execute(
            "INSERT INTO results (student_id, subject, marks, max_marks) VALUES (%s,%s,%s,%s)",
            (sid, subject, marks, max_m)
        )
        conn.commit()
        print(f"Result added. Grade: {compute_grade(marks, max_m)}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close(); conn.close()


def view_results():
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.name, s.roll_number, r.subject, r.marks, r.max_marks
            FROM results r
            JOIN students s ON r.student_id = s.id
            ORDER BY s.name, r.subject
        """)
        rows = cursor.fetchall()
        if not rows:
            print("No results found."); return
        print(f"\n{'Name':<22} {'Roll':<12} {'Subject':<20} {'Marks':>8}  Grade")
        print("─" * 70)
        for row in rows:
            grade = compute_grade(row[3], row[4])
            print(f"{row[0]:<22} {row[1]:<12} {row[2]:<20} {row[3]:>5}/{row[4]:<5}  {grade}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close(); conn.close()


def student_transcript():
    view_students()
    try:
        sid    = int(input("\nEnter Student ID: "))
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, roll_number, department FROM students WHERE id=%s", (sid,))
        stu = cursor.fetchone()
        if not stu:
            print("Student not found."); return
        cursor.execute(
            "SELECT subject, marks, max_marks FROM results WHERE student_id=%s", (sid,)
        )
        results = cursor.fetchall()
        print("\n" + "=" * 50)
        print(f"  ACADEMIC TRANSCRIPT")
        print("=" * 50)
        print(f"  Name       : {stu[0]}")
        print(f"  Roll No    : {stu[1]}")
        print(f"  Department : {stu[2]}")
        print("─" * 50)
        print(f"  {'Subject':<22} {'Marks':>8}   Grade")
        print("─" * 50)
        total = total_max = 0
        for r in results:
            grade = compute_grade(r[1], r[2])
            print(f"  {r[0]:<22} {r[1]:>5}/{r[2]:<5}  {grade}")
            total += r[1]; total_max += r[2]
        if results:
            overall = compute_grade(total, total_max)
            pct     = (total / total_max * 100) if total_max else 0
            print("─" * 50)
            print(f"  {'Total':<22} {total:>5}/{total_max:<5}  {overall}")
            print(f"  Percentage : {pct:.2f}%")
        print("=" * 50)
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close(); conn.close()


# ── Main Menu ─────────────────────────────────
def main():
    print("=" * 45)
    print("   Student Result Management System")
    print("=" * 45)

    try:
        setup_database()
    except Error as e:
        print(f"DB setup failed: {e}\nEnsure MySQL is running and credentials are correct.")
        return

    menu = {
        "1": ("Add student",          add_student),
        "2": ("View all students",    view_students),
        "3": ("Delete student",       delete_student),
        "4": ("Add result/marks",     add_result),
        "5": ("View all results",     view_results),
        "6": ("Print transcript",     student_transcript),
        "7": ("Exit",                 None),
    }

    while True:
        print("\n--- MENU ---")
        for k, (label, _) in menu.items():
            print(f"  {k}. {label}")
        choice = input("Choose: ").strip()
        if choice == "7":
            print("Goodbye!"); break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
