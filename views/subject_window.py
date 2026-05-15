import tkinter as tk
from tkinter import ttk

GRADE_COLORS = {
    "HD": "#7c3aed",
    "D":  "#2563eb",
    "C":  "#0891b2",
    "P":  "#16a34a",
    "F":  "#dc2626",
}


class SubjectWindow(tk.Toplevel):
    """
    Window 3 — Subject Details (modal).
    Lists all enrolled subjects and shows a summary panel.
    """

    def __init__(self, parent, student):
        super().__init__(parent)
        self.student = student
        self.title("Enrolled Subjects")
        self.resizable(False, False)
        self.configure(bg="white")
        self.grab_set()
        self.focus_set()
        self._style()
        self._build()
        self._center(parent)
        self.bind("<Escape>", lambda _: self.destroy())

    def _style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("S.Treeview",
                    font=("Arial", 10), rowheight=28,
                    background="white", fieldbackground="white",
                    foreground="#0f172a")
        s.configure("S.Treeview.Heading",
                    font=("Arial", 10, "bold"),
                    background="#1e40af", foreground="white", relief="flat")
        s.map("S.Treeview",
              background=[("selected", "#dbeafe")],
              foreground=[("selected", "#0f172a")])

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg="#1e40af", padx=20, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Enrolled Subjects",
                 font=("Arial", 13, "bold"), fg="white", bg="#1e40af").pack(anchor="w")
        tk.Label(hdr, text=f"{self.student.name}  ·  ID: {self.student.id}",
                 font=("Arial", 9), fg="#bfdbfe", bg="#1e40af").pack(anchor="w")

        # Table
        tbl = tk.Frame(self, bg="white", padx=20, pady=14)
        tbl.pack(fill="both", expand=True)

        height = max(len(self.student.subjects), 1)
        tree = ttk.Treeview(tbl, columns=("id", "mark", "grade"),
                            show="headings", style="S.Treeview", height=height)
        tree.heading("id",    text="Subject ID")
        tree.heading("mark",  text="Mark")
        tree.heading("grade", text="Grade")
        tree.column("id",    width=160, anchor="center")
        tree.column("mark",  width=120, anchor="center")
        tree.column("grade", width=120, anchor="center")

        for grade, color in GRADE_COLORS.items():
            tree.tag_configure(grade, foreground=color)

        if self.student.subjects:
            for subj in self.student.subjects:
                tree.insert("", "end",
                            values=(subj.id, subj.mark, subj.grade),
                            tags=(subj.grade,))
        else:
            tree.insert("", "end", values=("—", "—", "—"))

        tree.pack(fill="x")

        # Summary cards
        avg    = self.student.get_average_mark()
        grade  = self.student.get_grade()
        passed = self.student.is_pass()

        summary = tk.Frame(self, bg="#f1f5f9", padx=20, pady=14)
        summary.pack(fill="x")

        cards = [
            ("Average Mark", f"{avg:.2f}" if self.student.subjects else "—", "#1e40af"),
            ("Grade",        grade if self.student.subjects else "—",
             GRADE_COLORS.get(grade, "#374151")),
            ("Subjects",     f"{len(self.student.subjects)} / 4",              "#374151"),
            ("Status",       ("PASS" if passed else "FAIL") if self.student.subjects else "—",
             "#16a34a" if passed else "#dc2626"),
        ]

        for label, value, color in cards:
            card = tk.Frame(summary, bg="white", padx=12, pady=8)
            card.pack(side="left", expand=True, fill="x", padx=(0, 8))
            tk.Label(card, text=label, font=("Arial", 8),
                     fg="#94a3b8", bg="white").pack()
            tk.Label(card, text=value, font=("Arial", 13, "bold"),
                     fg=color, bg="white").pack()

        # Close button
        btn_frame = tk.Frame(self, bg="white", padx=20, pady=12)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Close",
                  font=("Arial", 10, "bold"),
                  bg="#1e40af", fg="white", activebackground="#1e3a8a",
                  relief="flat", padx=18, pady=6, cursor="hand2",
                  command=self.destroy).pack(anchor="e")

    def _center(self, parent):
        self.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width()  // 2 - self.winfo_width()  // 2
        y = parent.winfo_rooty() + parent.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")
