import tkinter as tk
from models.database import Database
from utils.validators import validate_credentials
from views.exception_window import ExceptionWindow


class LoginWindow(tk.Toplevel):
    """
    Window 1 — Login.
    Students enter email + password to reach the Enrolment window.
    """

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.title("GUIUniApp — Login")
        self.geometry("440x520")
        self.resizable(False, False)
        self.configure(bg="#1e40af")
        self.protocol("WM_DELETE_WINDOW", self._quit)
        self._build()
        self._center()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg="#1e40af", pady=30)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🎓", font=("Arial", 34), bg="#1e40af", fg="white").pack()
        tk.Label(hdr, text="GUIUniApp", font=("Arial", 20, "bold"),
                 fg="white", bg="#1e40af").pack()
        tk.Label(hdr, text="University Enrolment System",
                 font=("Arial", 10), fg="#bfdbfe", bg="#1e40af").pack(pady=(2, 0))

        # White card
        card = tk.Frame(self, bg="white", padx=36, pady=28)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="Student Login", font=("Arial", 14, "bold"),
                 fg="#1e293b", bg="white").pack(anchor="w")
        tk.Label(card, text="Sign in with your university credentials",
                 font=("Arial", 9), fg="#94a3b8", bg="white").pack(anchor="w", pady=(2, 18))

        # Email
        tk.Label(card, text="Email Address", font=("Arial", 9, "bold"),
                 fg="#374151", bg="white").pack(anchor="w")
        self.email_var = tk.StringVar()
        self._email_entry = tk.Entry(card, textvariable=self.email_var,
                                     font=("Arial", 11), relief="solid", bd=1)
        self._email_entry.pack(fill="x", ipady=7, pady=(3, 12))
        self._email_entry.focus()

        # Password
        tk.Label(card, text="Password", font=("Arial", 9, "bold"),
                 fg="#374151", bg="white").pack(anchor="w")
        self.pass_var = tk.StringVar()
        tk.Entry(card, textvariable=self.pass_var, show="●",
                 font=("Arial", 11), relief="solid", bd=1).pack(
                     fill="x", ipady=7, pady=(3, 20))

        # Login button
        tk.Button(card, text="Login", font=("Arial", 11, "bold"),
                  bg="#1e40af", fg="white", activebackground="#1e3a8a",
                  relief="flat", pady=10, cursor="hand2",
                  command=self._login).pack(fill="x")

        # Inline status
        self.status_var = tk.StringVar()
        tk.Label(card, textvariable=self.status_var,
                 font=("Arial", 9), fg="#dc2626", bg="white",
                 wraplength=340).pack(pady=(8, 0))

        # Hint
        tk.Label(card,
                 text="Email:     firstname.lastname@university.com\n"
                      "Password:  Uppercase · 6+ letters · 3+ digits",
                 font=("Arial", 8), fg="#cbd5e1", bg="white",
                 justify="left").pack(anchor="w", pady=(10, 0))

        self.bind("<Return>", lambda _: self._login())

    # ── Logic ─────────────────────────────────────────────────────────────────

    def _login(self):
        email    = self.email_var.get().strip()
        password = self.pass_var.get().strip()

        if not email or not password:
            ExceptionWindow(self, "Empty Fields",
                            "Both email and password are required.")
            return

        if not validate_credentials(email, password):
            ExceptionWindow(self, "Invalid Format",
                            "Email or password format is incorrect.\n\n"
                            "Email:     firstname.lastname@university.com\n"
                            "Password:  Uppercase · 6+ letters · 3+ digits")
            return

        students = Database.load()
        student  = next(
            (s for s in students if s.email == email and s.password == password),
            None
        )
        if not student:
            ExceptionWindow(self, "Login Failed",
                            "No student found with those credentials.\n"
                            "Please check your email and password.")
            return

        # Success — hide login, open enrolment window
        self.withdraw()
        from views.enrolment_window import EnrolmentWindow
        EnrolmentWindow(self, student)

    def _quit(self):
        self.root.destroy()

    def _center(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w  = self.winfo_width()
        h  = self.winfo_height()
        self.geometry(f"+{(sw - w)//2}+{(sh - h)//2}")
