import tkinter as tk
from frames.CustomFrame import BlackFrame


class SettingsFrame(BlackFrame):

    def __init__(self, parent, app=None):
        super().__init__(parent)

        self.app = app

        self.build()

    def build(self):

        txt_color = "orange"

        self.title = tk.Label(self, text="SETTINGS", fg=txt_color)
        self.title.pack()

        self.can_lbl = tk.Label(self, text="CAN", fg=txt_color)
        self.can_lbl.pack()

        self.can_btn = tk.Button(self, text="OFF", fg=txt_color, command=lambda: self.btn_pressed("CAN"))
        self.can_btn.pack()

        self.trip_reset_btn = tk.Button(self, text="RESET TRIP", fg=txt_color, command=lambda: self.btn_pressed("TRIP"))
        self.trip_reset_btn.pack()

    def btn_pressed(self, btn):

        action = None

        if btn == "CAN":
            if self.can_btn.cget("relief") == tk.SUNKEN:
                self.can_btn.config(relief=tk.RAISED, text="OFF")
                action = "CAN_OFF"
            else:
                self.can_btn.config(relief=tk.SUNKEN, text="ON")
                action = "CAN_ON"

        elif btn == "TRIP":
            action = "TRIP_RESET"

        if action is not None and self.app is not None:
            self.app.on_user_action(action)