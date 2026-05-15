import tkinter as tk


class ExceptionWindow(tk.Toplevel):
    """Modal error / warning popup."""

    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title("Notice")
        self.resizable(False, False)
        self.configure(bg="white")
        self.grab_set()
        self.focus_set()
        self._build(title, message)
        self._center(parent)
        self.bind("<Return>", lambda _: self.destroy())
        self.bind("<Escape>", lambda _: self.destroy())

    def _build(self, title, message):
        tk.Frame(self, bg="#dc2626", height=5).pack(fill="x")

        body = tk.Frame(self, bg="white", padx=28, pady=20)
        body.pack(fill="both", expand=True)

        row = tk.Frame(body, bg="white")
        row.pack(anchor="w", pady=(0, 6))
        tk.Label(row, text="⚠", font=("Arial", 18), fg="#dc2626", bg="white").pack(side="left", padx=(0, 10))
        tk.Label(row, text=title, font=("Arial", 12, "bold"), fg="#dc2626", bg="white").pack(side="left")

        tk.Frame(body, bg="#e5e7eb", height=1).pack(fill="x", pady=6)

        tk.Label(body, text=message, font=("Arial", 10), fg="#374151",
                 bg="white", justify="left", wraplength=300).pack(anchor="w", pady=(4, 18))

        tk.Button(body, text="  OK  ", font=("Arial", 10, "bold"),
                  bg="#dc2626", fg="white", activebackground="#b91c1c",
                  relief="flat", padx=4, pady=6, cursor="hand2",
                  command=self.destroy).pack(anchor="e")

    def _center(self, parent):
        self.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width()  // 2 - self.winfo_width()  // 2
        y = parent.winfo_rooty() + parent.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")
