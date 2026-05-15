# GUIUniApp 🎓

A desktop GUI application built with Python and Tkinter for the UTS FEIT Assessment 1 – Part 2.  
Designed for registered students to log in and manage their subject enrolments through a clean visual interface.

---

## 📁 Project Structure

```
GUIUniApp/
├── app.py                          # Entry point — launches the login window
├── seed.py                         # Populates students.data with test data
├── models/
│   ├── student.py                  # Student model (ID, name, email, password, subjects)
│   ├── subject.py                  # Subject model (ID, mark, grade)
│   └── database.py                 # Reads/writes students.data via pickle
├── utils/
│   └── validators.py               # Email and password regex validation
└── views/
    ├── login_window.py             # Window 1 — login screen
    ├── enrolment_window.py         # Window 2 — student dashboard (enrol/remove subjects)
    ├── subject_window.py           # Window 3 — subject details popup
    ├── change_password_window.py   # Window 4 — change password form
    └── exception_window.py         # Window 5 — error/warning popup
```

---

## 🚀 Getting Started

### Requirements

- Python **3.8+**
- **Tkinter** — bundled with Python, no extra install needed

### Run the app

```bash
# Step 1 — seed the database with test students (run once)
python seed.py

# Step 2 — launch the app
python app.py
```

---

## 🪟 Windows

### 1 — Login Window
The first screen. Enter a registered email and password to sign in.

- Checks that fields are not empty
- Validates email and password format via regex
- Verifies credentials against `students.data`
- Opens the **Enrolment Window** on success

### 2 — Enrolment Window
The main student dashboard after login.

| Feature | Description |
|---|---|
| Stats strip | Live Average Mark, Grade, Pass/Fail, and subject count |
| Subject table | All enrolled subjects with colour-coded grades |
| Enrol | Adds a new randomly-assigned subject (mark 25–100) — up to 4 |
| Remove Selected | Select a row in the table, then click Remove |
| View Subjects | Opens the Subject Window popup |
| Change Password | Opens the Change Password form |
| Logout | Returns to the Login screen with fields cleared |

### 3 — Subject Window
A read-only modal popup listing all enrolled subjects and a summary panel showing Average Mark, Grade, Subject count, and Pass/Fail status.

### 4 — Change Password Window
A modal form for updating the student password.
- Validates the new password format
- Both fields must match before saving
- Shows a green success confirmation on update

### 5 — Exception Window
A modal error popup shown whenever something goes wrong:
- Empty login fields
- Invalid email or password format
- Wrong login credentials
- Attempting to enrol in more than 4 subjects
- Attempting to remove without selecting a row

---

## ✅ Validation Rules

| Field | Rule |
|---|---|
| Email | `firstname.lastname@university.com` |
| Password | Starts with uppercase · 6+ letters · ends with 3+ digits |

**Example:** `Helloworld123` ✅ &nbsp;&nbsp; `Hello123` ❌ (too few letters)

---

## 🎨 Grade Colour Coding

| Grade | Meaning | Mark Range | Colour |
|---|---|---|---|
| HD | High Distinction | ≥ 85 | Purple |
| D  | Distinction      | ≥ 75 | Blue |
| C  | Credit           | ≥ 65 | Cyan |
| P  | Pass             | ≥ 50 | Green |
| F  | Fail             | < 50 | Red |

---

## 💾 Data

Student data is stored locally in `students.data` using Python's `pickle` module.  
Run `seed.py` once to populate it with the five test accounts below.

| Name | Email | Password | Subjects | Grade |
|---|---|---|---|---|
| John Smith | john.smith@university.com | Helloworld123 | 4 | C |
| Alen Jones | alen.jones@university.com | Helloworld123 | 3 | P |
| Sarah Connor | sarah.connor@university.com | Skynet2029 | 4 | HD |
| Bruce Wayne | bruce.wayne@university.com | Batman2099 | 2 | F |
| Diana Prince | diana.prince@university.com | Wonder123 | 3 | D |
