import json
#import cv2
import numpy as np
import os

def hex_to_rgb(hex_color):
    # Convert hex color to RGB
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


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

    BL_PRESET_NAMES = ["OFF", "priorities"]

    def __init__(self, parent):

        self.path = "presets.json"
        self.storage = {}
        self.load_last_presets()

        self.parent = parent



    def save_preset(self, name, leds):

        if name in self.BL_PRESET_NAMES:
            return False

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

        if preset_name + '.jpg' in os.listdir(self.parent.server.PRESET_IMG_LOCATION):
            os.remove(os.path.join(self.parent.server.PRESET_IMG_LOCATION, preset_name + '.jpg'))

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


    def create_preset_img(self, name):

        colors = None

        if name in self.storage.keys():
            try:
                colors = [x['color'] for x in self.storage[name]]
            except KeyError as e:
                print(str(e))
                return False

        if colors is None: return False
        print(colors)

        image_size = (30, 100, 3)

        # Create a blank image
        image = np.ones(image_size, dtype=np.uint8) * 255  # White background

        # Calculate the width of each color block
        block_width = image_size[1] // len(colors)

        # Draw each color block on the image
        for i, color in enumerate(colors):
            start_col = i * block_width
            end_col = (i + 1) * block_width
            image[:, start_col:end_col, :] = hex_to_rgb(color)

        # Save the image with the preset name
        image_filename = f"static/preset_images/{name}.jpg"
        #cv2.imwrite(image_filename, image)
        return False
        return True

class App(object):

    def __init__(self):

        self.server = None
        self.ui = None

        self.leds = [
            LEDObject('left_outer', '#808080', 0),
            LEDObject('left_inner', '#808080', 0),
            LEDObject('right_inner', '#808080', 0),
            LEDObject('right_outer', '#808080', 0),
            LEDObject('lower_left', '#808080', 0),
            LEDObject('lower_right', '#808080', 0)
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
