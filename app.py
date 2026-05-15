import tkinter as tk
from views.login_window import LoginWindow


def main():
    root = tk.Tk()
    root.withdraw()          # hide root; LoginWindow uses its own Toplevel
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
