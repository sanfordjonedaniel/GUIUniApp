"""
Populates students.data with pre-registered students and enrolled subjects.
These credentials work for GUIUniApp login.

    python seed.py

Run this from inside the GUIUniApp folder.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from models.student import Student
from models.subject import Subject
from models.database import Database


def make_subject(mark):
    s = Subject()
    s.mark = mark
    s.grade = s._calculate_grade()
    return s


SEED_DATA = [
    {
        "name": "John Smith",
        "email": "john.smith@university.com",
        "password": "Helloworld123",
        "marks": [72, 68, 75, 80],
    },
    {
        "name": "Alen Jones",
        "email": "alen.jones@university.com",
        "password": "Helloworld123",
        "marks": [55, 48, 60],
    },
    {
        "name": "Sarah Connor",
        "email": "sarah.connor@university.com",
        "password": "Skynet2029",
        "marks": [90, 88, 95, 92],
    },
    {
        "name": "Bruce Wayne",
        "email": "bruce.wayne@university.com",
        "password": "Batman2099",
        "marks": [30, 40],
    },
    {
        "name": "Diana Prince",
        "email": "diana.prince@university.com",
        "password": "Wonder123",
        "marks": [78, 82, 76],
    },
]


def seed():
    students = []
    for entry in SEED_DATA:
        student = Student(entry["name"], entry["email"], entry["password"])
        existing_ids = set()
        for mark in entry["marks"]:
            sub = make_subject(mark)
            while sub.id in existing_ids:
                sub = make_subject(mark)
            existing_ids.add(sub.id)
            student.subjects.append(sub)
        students.append(student)

    Database.save(students)
    print(f"Seeded {len(students)} students into students.data")
    print()
    for s in students:
        avg = s.get_average_mark()
        print(f"  {s.name:<16} | ID: {s.id} | {len(s.subjects)} subjects "
              f"| Avg: {avg:.2f} | Grade: {s.get_grade()} | "
              f"{'PASS' if s.is_pass() else 'FAIL'}")
    print()
    print("You can now log in to GUIUniApp with any of the above accounts.")
    print("All passwords are listed in the README.")


if __name__ == "__main__":
    seed()
