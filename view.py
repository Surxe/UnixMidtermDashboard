import tkinter as tk

class View:
    def __init__(self, root, controller) -> None:
        self.frame = tk.Frame(root)
        self.controller = controller
        self.titleLabel = tk.Label(master=root, font=("Helvetica", 22, "bold"), text="System Administration using UNIX Midterm Project")

    def pack_widgets(self):
        self.titleLabel.pack(pady=5)