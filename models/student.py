import random


class Student:
    def __init__(self, name, email, password):
        self.id = f"{random.randint(1, 999999):06d}"
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    def get_average_mark(self):
        if not self.subjects:
            return 0.0
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def get_grade(self):
        avg = self.get_average_mark()
        if avg >= 85:
            return 'HD'
        elif avg >= 75:
            return 'D'
        elif avg >= 65:
            return 'C'
        elif avg >= 50:
            return 'P'
        else:
            return 'F'

    def is_pass(self):
        return self.get_average_mark() >= 50
