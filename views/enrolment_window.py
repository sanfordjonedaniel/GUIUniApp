import tkinter as tk
from tkinter import ttk
from models.subject import Subject
from models.database import Database
from views.exception_window import ExceptionWindow

MAX_SUBJECTS = 4

GRADE_COLORS = {
    "HD": "#7c3aed",
    "D":  "#2563eb",
    "C":  "#0891b2",
    "P":  "#16a34a",
    "F":  "#dc2626",
}


class EnrolmentWindow(tk.Toplevel):
    """
    Window 2 — Student Dashboard.
    Enrol / remove subjects, view details, change password, logout.
    """

    def __init__(self, login_win, student):
        super().__init__(login_win)
        self.login_win = login_win   # keep reference to restore on logout
        self.student   = student
        self.title("GUIUniApp — Enrolment")
        self.geometry("580x580")
        self.resizable(False, False)
        self.configure(bg="#f8fafc")
        self.protocol("WM_DELETE_WINDOW", self._logout)
        self._style()
        self._build()
        self._refresh()
        self._center()

    # ── Treeview style ────────────────────────────────────────────────────────

    def _style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("T.Treeview",
                    font=("Arial", 10), rowheight=30,
                    background="white", fieldbackground="white",
                    foreground="#0f172a")
        s.configure("T.Treeview.Heading",
                    font=("Arial", 10, "bold"),
                    background="#1e40af", foreground="white", relief="flat")
        s.map("T.Treeview",
              background=[("selected", "#dbeafe")],
              foreground=[("selected", "#0f172a")])

    # ── Build UI ──────────────────────────────────────────────────────────────

    def _build(self):
        # ── Blue header ───────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg="#1e40af", padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"Welcome, {self.student.name}",
                 font=("Arial", 14, "bold"), fg="white", bg="#1e40af").pack(anchor="w")
        tk.Label(hdr, text=f"ID: {self.student.id}  ·  {self.student.email}",
                 font=("Arial", 9), fg="#bfdbfe", bg="#1e40af").pack(anchor="w")

        # ── Stats strip ───────────────────────────────────────────────────────
        stats = tk.Frame(self, bg="#1e3a8a", padx=20, pady=10)
        stats.pack(fill="x")
        self.lbl_avg    = self._stat(stats, "Average Mark", "—")
        self.lbl_grade  = self._stat(stats, "Grade",        "—")
        self.lbl_status = self._stat(stats, "Status",       "—")
        self.lbl_slots  = self._stat(stats, "Subjects",     f"0 / {MAX_SUBJECTS}")

        # ── Subject table ─────────────────────────────────────────────────────
        tbl_frame = tk.Frame(self, bg="white", padx=20, pady=14)
        tbl_frame.pack(fill="both", expand=True)

        tk.Label(tbl_frame, text="Enrolled Subjects",
                 font=("Arial", 10, "bold"), fg="#374151", bg="white").pack(anchor="w", pady=(0, 6))

        self.tree = ttk.Treeview(tbl_frame,
                                 columns=("id", "mark", "grade"),
                                 show="headings",
                                 style="T.Treeview",
                                 height=7)
        self.tree.heading("id",    text="Subject ID")
        self.tree.heading("mark",  text="Mark")
        self.tree.heading("grade", text="Grade")
        self.tree.column("id",    width=200, anchor="center")
        self.tree.column("mark",  width=150, anchor="center")
        self.tree.column("grade", width=150, anchor="center")
        self.tree.pack(fill="x")

        for grade, color in GRADE_COLORS.items():
            self.tree.tag_configure(grade, foreground=color)

        # ── Buttons ───────────────────────────────────────────────────────────
        row1 = tk.Frame(self, bg="#f8fafc", padx=20)
        row1.pack(fill="x", pady=(12, 4))

        tk.Button(row1, text="＋  Enrol in Subject",
                  font=("Arial", 10, "bold"),
                  bg="#16a34a", fg="white", activebackground="#15803d",
                  relief="flat", padx=14, pady=8, cursor="hand2",
                  command=self._enrol).pack(side="left", padx=(0, 8))

        tk.Button(row1, text="－  Remove Selected",
                  font=("Arial", 10, "bold"),
                  bg="#dc2626", fg="white", activebackground="#b91c1c",
                  relief="flat", padx=14, pady=8, cursor="hand2",
                  command=self._remove).pack(side="left", padx=(0, 8))

        tk.Button(row1, text="View Subjects",
                  font=("Arial", 10, "bold"),
                  bg="#1e40af", fg="white", activebackground="#1e3a8a",
                  relief="flat", padx=14, pady=8, cursor="hand2",
                  command=self._view_subjects).pack(side="left")

        row2 = tk.Frame(self, bg="#f8fafc", padx=20)
        row2.pack(fill="x", pady=(0, 16))

        tk.Button(row2, text="Change Password",
                  font=("Arial", 10),
                  bg="#f59e0b", fg="white", activebackground="#d97706",
                  relief="flat", padx=14, pady=7, cursor="hand2",
                  command=self._change_password).pack(side="left")

        tk.Button(row2, text="Logout",
                  font=("Arial", 10),
                  bg="#e2e8f0", fg="#374151", activebackground="#cbd5e1",
                  relief="flat", padx=14, pady=7, cursor="hand2",
                  command=self._logout).pack(side="right")

    # ── Stat widget helper ────────────────────────────────────────────────────

    def _stat(self, parent, label, value):
        box = tk.Frame(parent, bg="#1e3a8a", padx=12)
        box.pack(side="left", expand=True)
        tk.Label(box, text=label, font=("Arial", 7), fg="#93c5fd", bg="#1e3a8a").pack()
        lbl = tk.Label(box, text=value, font=("Arial", 12, "bold"),
                       fg="white", bg="#1e3a8a")
        lbl.pack()
        return lbl

    # ── Enrol ─────────────────────────────────────────────────────────────────

    def _enrol(self):
        if len(self.student.subjects) >= MAX_SUBJECTS:
            ExceptionWindow(self, "Limit Reached",
                            f"You are already enrolled in {MAX_SUBJECTS} subjects.\n"
                            "Students cannot enrol in more than 4 subjects.")
            return

        # Generate a subject with a unique ID
        existing_ids = {s.id for s in self.student.subjects}
        subject = Subject()
        while subject.id in existing_ids:
            subject = Subject()

        self.student.subjects.append(subject)
        self._save()
        self._refresh()

    # ── Remove ────────────────────────────────────────────────────────────────

    def _remove(self):
        selected = self.tree.selection()
        if not selected:
            ExceptionWindow(self, "Nothing Selected",
                            "Click on a subject row first, then press Remove.")
            return

        subject_id = self.tree.item(selected[0], "values")[0]
        self.student.subjects = [s for s in self.student.subjects if s.id != subject_id]
        self._save()
        self._refresh()

    # ── View subjects popup ───────────────────────────────────────────────────

    def _view_subjects(self):
        from views.subject_window import SubjectWindow
        SubjectWindow(self, self.student)

    # ── Change password popup ─────────────────────────────────────────────────

    def _change_password(self):
        from views.change_password_window import ChangePasswordWindow
        ChangePasswordWindow(self, self.student)

    # ── Logout ────────────────────────────────────────────────────────────────

    def _logout(self):
        self.destroy()
        self.login_win.email_var.set("")
        self.login_win.pass_var.set("")
        self.login_win.deiconify()

    # ── Refresh table + stats ─────────────────────────────────────────────────

    def _refresh(self):
        count = len(self.student.subjects)
        avg   = self.student.get_average_mark()
        grade = self.student.get_grade()
        gc    = GRADE_COLORS.get(grade, "white")

        self.lbl_avg.config(text=f"{avg:.2f}" if count else "—")
        self.lbl_grade.config(text=grade if count else "—", fg=gc)

        passed = self.student.is_pass()
        self.lbl_status.config(
            text=("PASS" if passed else "FAIL") if count else "—",
            fg="#86efac" if passed else "#fca5a5"
        )
        self.lbl_slots.config(text=f"{count} / {MAX_SUBJECTS}")

        # Rebuild table
        for row in self.tree.get_children():
            self.tree.delete(row)
        for subj in self.student.subjects:
            self.tree.insert("", "end",
                             values=(subj.id, subj.mark, subj.grade),
                             tags=(subj.grade,))

    # ── Save student back to database ─────────────────────────────────────────

    def _save(self):
        all_students = Database.load()
        for i, s in enumerate(all_students):
            if s.id == self.student.id:
                all_students[i] = self.student
                break
        Database.save(all_students)

    def _center(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"+{(sw - self.winfo_width())//2}+{(sh - self.winfo_height())//2}")
