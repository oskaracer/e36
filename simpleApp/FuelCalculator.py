import os
import json
from datetime import datetime, timedelta

STORAGE = "data/fuel.json"
HISTORY_STORAGE = "data/fuel_history.json"

class FuelCalculator:

    def __init__(self):

        # Storage info
        self.currentFuel = 0
        self.currentOdo = 0
        self.tripOdoStart = 0
        self.tripFuelStart = 0

        # Calculated
        self.trip_avg_consumption = 0
        self.km_left = 0

        self.last_saved_time = datetime.now()

        self.check_storage()

    def check_storage(self):

        if not os.path.exists(STORAGE):
            print("Storage not found. Creating...")
            os.makedirs(os.path.dirname(STORAGE), exist_ok=True)
            storage = {
                "currentOdo": 0,
                "currentFuel": 0,
                "tripOdoStart": 0,
                "tripFuelStart": 0
            }

            with open(STORAGE, "w") as f:
                f.write(json.dumps(storage, indent=4))


    def get_km_left(self): return self.km_left
    def get_currentFuel(self): return self.currentFuel
    def get_avg_consumption(self): return self.trip_avg_consumption

    def on_new_data(self, data):

        for k, v in data.items():

            if k == "currentFuel":
                self.currentFuel = v
            elif k == "currentOdo":
                self.currentOdo = v

        print("FUELCLACULATOR: TODO: Update all values | save every MINUTE | CHECK if FUEL IS BECOME MORE - ZAPRAVKA")

    def start_trip(self):

        self.save_past_data()

        self.tripOdoStart = self.currentOdo
        self.tripFuelStart = self.tripFuelStart
        self.km_left = 0
        self.trip_avg_consumption = 0

    def save_past_data(self):

        if datetime.now() - self.last_saved_time < timedelta(seconds=3):
            print("Fuel already saved!")
            return False

        curr_history = {}

        if not os.path.exists(HISTORY_STORAGE):
            os.makedirs(os.path.dirname(HISTORY_STORAGE), exist_ok=True)
        else:
            with open(HISTORY_STORAGE, "r") as f:
                curr_history = json.load(f)

        new_record = {
                "currentOdo": self.currentOdo,
                "currentFuel": self.currentFuel,
                "tripOdoStart": self.tripOdoStart,
                "tripFuelStart": self.tripFuelStart,
                "trip_avg_consumption": self.trip_avg_consumption,
                "km_left": self.km_left
        }
        curr_history.update({datetime.now().strftime("%Y-%m-%d %H:%M:%S"): new_record})

        with open(HISTORY_STORAGE, "w") as f:
            f.write(json.dumps(curr_history, indent=4))

        self.last_saved_time = datetime.now()
        print(f"SAVED TO HISTORY: {new_record} at {self.last_saved_time}")

        return True

    def save_curr_data(self):

        if not os.path.exists(STORAGE):
            print("Storage not found. Creating...")
            os.makedirs(os.path.dirname(STORAGE), exist_ok=True)

        storage = {
            "currentOdo": self.currentOdo,
            "currentFuel": self.currentFuel,
            "tripOdoStart": self.tripOdoStart,
            "tripFuelStart": self.tripFuelStart,
            "trip_avg_consumption": self.trip_avg_consumption,
            "km_left": self.km_left
        }

        with open(STORAGE, "w") as f:
            f.write(json.dumps(storage, indent=4))