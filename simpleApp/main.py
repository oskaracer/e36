import tkinter as tk

from frames.InfoFrame import InfoFrame
from frames.SettingsFrame import SettingsFrame
from canInterface import CanInterface
from simpleApp.FuelCalculator import FuelCalculator

VCC_FRAME_POS=0,0

class App:
    def __init__(self, master):
        self.master = master
        self.setup_master()

        self.canIface = CanInterface("can0", self)
        self.canIface.start()
        self.fuelCalculator = FuelCalculator()



        self.frames = {}

        self.add_frame(InfoFrame(self.master), row=0, col=0)
        self.add_frame(SettingsFrame(self.master, self), row=1, col=0)

    def add_frame(self, frame, row, col):

        s = f"{row}:{col}"
        if s in self.frames.keys():
            print(f"Can't grid frame. Space already taken by: {self.frames[s]}")
            return False

        frame.grid(row=row, column=col)
        self.frames.update({s: frame})
        return True

    def setup_master(self):

        self.master.title("Orange Text App")
        self.master.geometry("400x200")
        self.master.configure(bg="black")

        self.master.bind("<Destroy>", lambda e: self.on_close())

    def on_close(self, event=None):

        print("Closing app...")
        self.canIface.stop()
        self.fuelCalculator.save_curr_data()

    def on_user_action(self, action):

        if action == "CAN_ON":
            self.canIface.paused = False
        elif action == "CAN_OFF":
            self.canIface.paused = True
        elif action == "TRIP_RESET":
            self.fuelCalculator.start_trip()

    def on_new_data(self, name, data):
        if name == "VCC":
            self.frames["0:0"].update_data(name, data)

        if name == "FUEL":
            self.fuelCalculator.on_new_data(data)
            self.frames["0:0"].update_data(name,
                                           {
                                               "left_l": self.fuelCalculator.get_currentFuel(),
                                               "left_km": self.fuelCalculator.get_km_left(),
                                               "avg_km_l": self.fuelCalculator.get_avg_consumption()
                                           })


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":

    main()


