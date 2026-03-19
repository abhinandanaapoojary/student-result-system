# Student Result Management System

A full-stack student result management application integrating Python backend with MySQL database to manage marks and auto-compute grades for 100+ student records.

## Features
- Add, view, and delete student records
- Add subject-wise marks for each student
- Automated grade computation (A+, A, B, C, D, F)
- Print complete academic transcript per student
- Normalized relational database schema (MySQL)
- Optimized SQL queries with JOIN operations

## Tech Stack
- Python 3
- MySQL (via mysql-connector-python)
- Relational database design (normalized schema)
- Modular programming

## Database Schema
```
students
  id (PK), name, roll_number (UNIQUE), department

results
  id (PK), student_id (FK), subject, marks, max_marks
```

## Grade Scale
| Percentage | Grade |
|------------|-------|
| 90 - 100   | A+    |
| 80 - 89    | A     |
| 70 - 79    | B     |
| 60 - 69    | C     |
| 50 - 59    | D     |
| Below 50   | F     |

## How to Run

### Step 1 — Install dependencies
```bash
pip install mysql-connector-python
```

### Step 2 — Setup MySQL
Make sure MySQL is running. Update the credentials in the script:
```python
password="your_password"   # line 16 and 21
```

### Step 3 — Run
```bash
python student_result_system.py
```
The database and tables are created automatically on first run.

## Sample Transcript Output
```
==================================================
  ACADEMIC TRANSCRIPT
==================================================
  Name       : Abhinandana
  Roll No    : 1VT23IS010
  Department : Information Science & Engineering
──────────────────────────────────────────────────
  Subject                Marks    Grade
──────────────────────────────────────────────────
  Data Structures         88/100   A
  DBMS                    92/100   A+
  Python Programming      95/100   A+
──────────────────────────────────────────────────
  Total                  275/300   A+
  Percentage : 91.67%
==================================================
```

## Developer
**Abhinandana A Poojary**
Information Science and Engineering, Vemana Institute of Technology
