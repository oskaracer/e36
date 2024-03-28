import tkinter as tk
from frames.CustomFrame import BlackFrame


class VoltageFrame(BlackFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.label = None

        self.build()

    def build(self):

        self.label = tk.Label(self, text="VCC: ", fg="orange", bg="black", font=("Helvetica", 24))
        self.label.pack(pady=50)

    def update_data(self, new_vcc):
        print("A")
        self.label.config(text=f"VCC: {new_vcc}")


class FuelFrame(BlackFrame):

    font = ("Helvetica", 12)

    def __init__(self, parent):
        super().__init__(parent)
        self.label = None
        self.label_l = None
        self.label_km = None
        self.label_kml = None

        self.build()

    def build(self):

        self.label = tk.Label(self, text="FUEL", fg="orange", bg="black", font=self.font)
        self.label.pack(pady=5)
        self.label_l = tk.Label(self, text="LEFT L: X", fg="orange", bg="black", font=self.font)
        self.label_l.pack(pady=5)
        self.label_km = tk.Label(self, text="LEFT KM: X", fg="orange", bg="black", font=self.font)
        self.label_km.pack(pady=5)
        self.label_kml = tk.Label(self, text="AVG KM/L: X", fg="orange", bg="black", font=self.font)
        self.label_kml.pack(pady=5)

    def update_data(self, new_data):
        # {left_l, left_km, avg_km_l}
        #new_data = {"left_l": 1, "left_km": 1, "avg_km_l": 1}
        self.label_l.config(text=f"LEFT L: {new_data['left_l']}")
        self.label_km.config(text=f"LEFT KM: {new_data['left_km']}")
        self.label_kml.config(text=f"AVG KM/L: {new_data['avg_km_l']}")


class InfoFrame(BlackFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.label = None

        self.vcc_frame = None
        self.fuel_frame = None

        self.build()

    def build(self):
        self.vcc_frame = VoltageFrame(self)
        self.vcc_frame.grid(row=0, column=0)

        self.fuel_frame = FuelFrame(self)
        self.fuel_frame.grid(row=0, column=1)

    def update_data(self, name, data):
        if name == "VCC":
            self.vcc_frame.update_data(data)
        elif name == "FUEL":
            self.fuel_frame.update_data(data)
