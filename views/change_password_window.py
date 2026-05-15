import tkinter as tk
from models.database import Database
from utils.validators import validate_password
from views.exception_window import ExceptionWindow


class ChangePasswordWindow(tk.Toplevel):
    """
    Window 4 — Change Password (modal).
    Validates format and confirms both fields match before saving.
    """

    def __init__(self, parent, student):
        super().__init__(parent)
        self.parent  = parent
        self.student = student
        self.title("Change Password")
        self.resizable(False, False)
        self.configure(bg="white")
        self.grab_set()
        self.focus_set()
        self._build()
        self._center(parent)
        self.bind("<Return>", lambda _: self._update())
        self.bind("<Escape>", lambda _: self.destroy())

    def _build(self):
        tk.Frame(self, bg="#f59e0b", height=5).pack(fill="x")

        hdr = tk.Frame(self, bg="#fffbeb", padx=20, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Change Password", font=("Arial", 13, "bold"),
                 fg="#92400e", bg="#fffbeb").pack(anchor="w")
        tk.Label(hdr,
                 text="Uppercase start  ·  6+ letters  ·  3+ digits",
                 font=("Arial", 8), fg="#b45309", bg="#fffbeb").pack(anchor="w")

        form = tk.Frame(self, bg="white", padx=24, pady=20)
        form.pack(fill="both", expand=True)

        # New password
        tk.Label(form, text="New Password", font=("Arial", 9, "bold"),
                 fg="#374151", bg="white").pack(anchor="w")
        self.new_var = tk.StringVar()
        new_entry = tk.Entry(form, textvariable=self.new_var,
                             font=("Arial", 11), show="●",
                             relief="solid", bd=1, width=30)
        new_entry.pack(anchor="w", ipady=6, pady=(3, 14))
        new_entry.focus()

        # Confirm password
        tk.Label(form, text="Confirm Password", font=("Arial", 9, "bold"),
                 fg="#374151", bg="white").pack(anchor="w")
        self.confirm_var = tk.StringVar()
        tk.Entry(form, textvariable=self.confirm_var,
                 font=("Arial", 11), show="●",
                 relief="solid", bd=1, width=30).pack(anchor="w", ipady=6, pady=(3, 20))

        # Buttons
        btns = tk.Frame(form, bg="white")
        btns.pack(fill="x")

        tk.Button(btns, text="Update Password",
                  font=("Arial", 10, "bold"),
                  bg="#f59e0b", fg="white", activebackground="#d97706",
                  relief="flat", padx=14, pady=7, cursor="hand2",
                  command=self._update).pack(side="left", padx=(0, 8))

        tk.Button(btns, text="Cancel",
                  font=("Arial", 10),
                  bg="#e2e8f0", fg="#374151",
                  relief="flat", padx=14, pady=7, cursor="hand2",
                  command=self.destroy).pack(side="left")

    def _update(self):
        new     = self.new_var.get().strip()
        confirm = self.confirm_var.get().strip()

        if not new or not confirm:
            ExceptionWindow(self, "Empty Fields", "Please fill in both fields.")
            return

        if not validate_password(new):
            ExceptionWindow(self, "Invalid Format",
                            "Password must:\n"
                            "  • Start with an uppercase letter\n"
                            "  • Contain at least 6 letters total\n"
                            "  • End with 3 or more digits\n\n"
                            "Example:  Helloworld123")
            return

        if new != confirm:
            ExceptionWindow(self, "Password Mismatch",
                            "The two passwords do not match.\nPlease try again.")
            return

        # Save
        self.student.password = new
        all_students = Database.load()
        for i, s in enumerate(all_students):
            if s.id == self.student.id:
                all_students[i] = self.student
                break
        Database.save(all_students)

        self.destroy()

        # Success popup
        ok = tk.Toplevel(self.parent)
        ok.title("Success")
        ok.resizable(False, False)
        ok.configure(bg="white")
        ok.grab_set()
        tk.Frame(ok, bg="#16a34a", height=5).pack(fill="x")
        f = tk.Frame(ok, bg="white", padx=24, pady=20)
        f.pack()
        tk.Label(f, text="✓  Password updated successfully!",
                 font=("Arial", 11, "bold"), fg="#16a34a", bg="white").pack(pady=(0, 14))
        tk.Button(f, text="OK", font=("Arial", 10, "bold"),
                  bg="#16a34a", fg="white", relief="flat",
                  padx=18, pady=6, cursor="hand2",
                  command=ok.destroy).pack(anchor="e")
        ok.bind("<Return>", lambda _: ok.destroy())
        ok.update_idletasks()
        x = self.parent.winfo_rootx() + self.parent.winfo_width()  // 2 - ok.winfo_width()  // 2
        y = self.parent.winfo_rooty() + self.parent.winfo_height() // 2 - ok.winfo_height() // 2
        ok.geometry(f"+{x}+{y}")

    def _center(self, parent):
        self.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width()  // 2 - self.winfo_width()  // 2
        y = parent.winfo_rooty() + parent.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")
