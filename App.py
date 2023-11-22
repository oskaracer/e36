import json


class LEDObject:
    def __init__(self, name, color, brightness):
        self.name = name
        self.color = color
        self.brightness = brightness

        self.pin = 0

    def to_dict(self):
        return {
            'name': self.name,
            'color': self.color,
            'brightness': self.brightness
        }

    def __str__(self):
        return f"Name: {self.name} Pin: {self.pin} color: {self.color} brightness: {self.brightness}"


class ExhaustFlap(object):

    def __init__(self, defState=False):
        self.state = defState

    def toggleExhaustFlap(self):
        print(f"Changing Exhaust flap state from {self.state} to {not self.state}...")
        self.state = not self.state


class LEDPresetStorage(object):

    def __init__(self, parent):

        self.path = "presets.json"
        self.storage = {}
        self.load_last_presets()

        self.parent = parent

    def save_preset(self, name, leds):

        print(f"Saving preset: {name}")
        self.load_last_presets()

        preset_values = [led.to_dict() for led in leds]
        self.storage[name] = preset_values
        self.save_to_file()

    def load_preset(self, preset_name, leds):

        print(f"Loading preset: {preset_name}")

        self.load_last_presets()
        if preset_name in self.storage:

            preset_values = self.storage[preset_name]
            for i, led in enumerate(leds):
                if i < len(preset_values):
                    led.brightness = preset_values[i]['brightness']
                    led.color = preset_values[i]['color']

            print(f"Preset {preset_name} loaded successfully!")
            return True
        return False

    def delete_preset(self, preset_name):

        if preset_name == "default":
            print("Can't delete default preset")
            return False

        print(f"Deleting preset: {preset_name}")

        self.load_last_presets()
        if preset_name in self.storage:

            self.storage.pop(preset_name)
            print(f"Preset {preset_name} deleted successfully!")
            with open(self.path, 'w') as file:
                json.dump(self.storage, file, indent=2)

            return True
        return False

    def load_last_presets(self):

        try:
            with open(self.path, 'r') as file:
                self.storage = json.load(file)
            return self.storage
        except FileNotFoundError:
            return {}

    def save_to_file(self):

        with open(self.path, 'w') as file:
            json.dump(self.storage, file, indent=2)


class App(object):

    def __init__(self):

        self.server = None
        self.ui = None

        self.leds = [
            LEDObject('left_outer', '#808080', 128),
            LEDObject('left_inner', '#808080', 128),
            LEDObject('right_inner', '#808080', 128),
            LEDObject('right_outer', '#808080', 128),
            LEDObject('lower_left', '#808080', 128),
            LEDObject('lower_right', '#808080', 128)
        ]

        self.exhaustFlap = ExhaustFlap(False)

        self.presets = LEDPresetStorage(self)
        self.curr_preset = None # "default"

    def set_curr_preset(self, p):

        self.curr_preset = p


        if p is not None:
            return self.presets.load_preset(p, self.leds)

        # If None we leave values as previous preset was set as was for server
        return True

    def get_curr_preset(self):

        if self.curr_preset is None:
            return "OFF"
        else:
            return self.curr_preset

    def change_led_state(self):
        print("TODO: Here we need to do HW work")
