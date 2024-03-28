import tkinter as tk


class BlackFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.config(bg="black")