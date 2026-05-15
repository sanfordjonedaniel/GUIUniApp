import random


class Subject:
    def __init__(self):
        self.id = f"{random.randint(1, 999):03d}"
        self.mark = random.randint(25, 100)
        self.grade = self._calculate_grade()

    def _calculate_grade(self):
        if self.mark >= 85:
            return 'HD'
        elif self.mark >= 75:
            return 'D'
        elif self.mark >= 65:
            return 'C'
        elif self.mark >= 50:
            return 'P'
        else:
            return 'F'
