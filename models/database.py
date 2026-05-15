import pickle
import os

# students.data lives in the GUIUniApp root folder (one level above this file)
_BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_FILE = os.path.join(_BASE_DIR, "students.data")


class Database:

    @staticmethod
    def load():
        if not os.path.exists(DATABASE_FILE):
            return []
        try:
            with open(DATABASE_FILE, "rb") as f:
                return pickle.load(f)
        except Exception:
            return []

    @staticmethod
    def save(students):
        with open(DATABASE_FILE, "wb") as f:
            pickle.dump(students, f)

    @staticmethod
    def clear():
        Database.save([])
