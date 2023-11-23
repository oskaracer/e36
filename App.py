import json
import cv2
import numpy as np
import os
from PyQt5.QtCore import pyqtSignal, QObject
from LedController import LEDController

def hex_to_bgr(hex_color):
    # Convert hex color to RGB
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (4, 2, 0))

    return rgb


class LEDObject:

    NAME2CAR_ICON_DATA = {

        "left_outer": {"pos": (405, 173), "radius": 18},
        "left_inner": {"pos": (365, 173), "radius": 18},
        "right_inner": {"pos": (127, 173), "radius": 18},
        "right_outer": {"pos": (87, 173), "radius": 18},

        "lower_left": {"pos": (49, 253, 99, 273), "radius": 3},
        "lower_right": {"pos": (392, 253, 442, 273), "radius": 3}

    }

    CIRCLES_NAMES = ["left_outer", "left_inner", "right_inner", "right_outer"]
    RECTS_NAMES = ["lower_left", "lower_right"]

    def __init__(self, name, color, brightness, animation=None):
        self.name = name
        self.color = color
        self.brightness = brightness
        self.animation = animation
        self.pin = 0

        try:
            self.car_icon_data = self.NAME2CAR_ICON_DATA[self.name]

        except Exception as e:
            print(str(e))
            self.car_icon_data = {"pos": (0, 0), "radius": 1}

    def to_dict(self):
        return {
            'name': self.name,
            'color': self.color,
            'brightness': self.brightness,
            'animation': self.animation
        }

    def __str__(self):
        return f"Name: {self.name} Pin: {self.pin} color: {self.color} brightness: {self.brightness}"


class ExhaustFlap(object):

    def __init__(self, defState=False):
        self.state = defState

    def toggleExhaustFlap(self):
        print(f"Exhaust flap state from {self.state} to {not self.state}...")
        self.state = not self.state


class LEDPresetStorage(object):
    BL_PRESET_NAMES = ["OFF", "shown_list"]

    PRESETS_LOCATION = "stored_data/presets.json"
    SELECTED_PRESETS_LOCATION = "stored_data/selected_presets"

    def __init__(self, parent):

        self.storage = {}
        self.selected_presets = []
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
                    try:
                        led.animation = preset_values[i]['animation']
                    except KeyError:
                        led.animation = None

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
            with open(self.PRESETS_LOCATION, 'w') as file:
                json.dump(self.storage, file, indent=2)

            return True

        if preset_name + '.jpg' in os.listdir(self.parent.server.PRESET_IMG_LOCATION):
            os.remove(os.path.join(self.parent.server.PRESET_IMG_LOCATION, preset_name + '.jpg'))

        return False

    def load_last_presets(self):

        try:
            with open(self.PRESETS_LOCATION, 'r') as file:
                self.storage = json.load(file)
            return self.storage
        except FileNotFoundError:
            return {}

    def save_to_file(self):

        with open(self.PRESETS_LOCATION, 'w') as file:
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

        image_size = (30, 200, 3)

        # Create a blank image
        image = np.ones(image_size, dtype=np.uint8) * 255  # White background

        # Calculate the width of each color block
        block_width = int(image_size[1] / len(colors))

        for i, color in enumerate(colors):

            if i > 3:

                cv2.rectangle(image,
                              pt1=(block_width * i, 0),
                              pt2=(block_width * i + block_width, image.shape[0]),
                              color=(hex_to_bgr(color)),
                              thickness=-1)

                cv2.rectangle(image,
                              pt1=(block_width * i, 0),
                              pt2=(block_width * i + block_width, image.shape[0] - 2),
                              color=(0, 0, 0),
                              thickness=2)
            else:

                cv2.circle(image,
                           center=(int(block_width / 2 + block_width * i), int(image.shape[0] / 2)),
                           radius=int(image.shape[0] / 2),
                           color=hex_to_bgr(color),
                           thickness=-1)
                cv2.circle(image,
                           center=(int(block_width / 2 + block_width * i), int(image.shape[0] / 2)),
                           radius=int(image.shape[0] / 2),
                           color=(0, 0, 0),
                           thickness=2)

        # Save the image with the preset name
        image_filename = f"static/preset_images/{name}.jpg"
        return cv2.imwrite(image_filename, image)

    def create_car_icon_preset(self, name):

        img_location = f"static/car_icon_{name}.jpg"

        img = cv2.imread("static/car_icon_default.jpg")
        if img is None:
            print("Couldn't load default car icon image!")
            return False

        for led in self.parent.leds:

            if led.name in LEDObject.CIRCLES_NAMES:

                cv2.circle(img, center=led.car_icon_data['pos'],
                           radius=led.car_icon_data['radius'],
                           color=hex_to_bgr(led.color),
                           thickness=-1)
            elif led.name in LEDObject.RECTS_NAMES:

                cv2.rectangle(img, pt1=(led.car_icon_data['pos'][0], led.car_icon_data['pos'][1]),
                              pt2=(led.car_icon_data['pos'][2], led.car_icon_data['pos'][3]),
                              color=hex_to_bgr(led.color),
                            thickness=-1)

        return cv2.imwrite(img_location, img)

    def load_selected_presets(self):
        try:
            with open(self.SELECTED_PRESETS_LOCATION, 'r') as file:
                self.selected_presets = file.readlines()
            return self.selected_presets
        except FileNotFoundError:
            return []

    # Mark preset to be shown local on monitor
    def markAsSelected(self, name):

        self.load_selected_presets()
        self.load_last_presets()

        for preset_name in self.selected_presets:

            if preset_name.strip() == name:
                print(f"Preset already marked: {name}")
                return False

        # If not marked yet
        if len(self.selected_presets) > 5:
            print(f"Removing oldest selected preset: {self.selected_presets[0]}")
            self.selected_presets.pop(0)

        self.selected_presets.append(name + "\n")
        with open(self.SELECTED_PRESETS_LOCATION, 'w') as f:
            f.writelines(self.selected_presets)

        print(f"new preset marked: {name}")
        self.parent.updateLedScreen.emit(f"update_ledscreen")
        return True

    def unmarkAsSelected(self, name):

        self.load_selected_presets()
        self.load_last_presets()

        to_remove = False
        for preset_name in self.selected_presets:

            if preset_name.strip() == name:
                to_remove = True

        if not to_remove:
            print(f"Preset {name} already doesn't exist in selected preset")
            return True

        self.selected_presets.remove(name + '\n')
        with open(self.SELECTED_PRESETS_LOCATION, 'w') as f:
            f.writelines(self.selected_presets)

        print(f"Selected preset removed: {name}")
        self.parent.updateLedScreen.emit(f"update_ledscreen")
        return True


class App(QObject):
    updateLedScreen = pyqtSignal(str)

    def __init__(self):

        super().__init__()
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
        self.ledController = LEDController(self)

        self.curr_preset = None  # "default"

    def set_curr_preset(self, p):

        self.curr_preset = p

        if p is not None:
            self.ledController.update_led_state()
            return self.presets.load_preset(p, self.leds)

        # If None we leave values as previous preset was set as was for server
        return True

    def get_curr_preset(self):

        if self.curr_preset is None:
            return "OFF"
        else:
            return self.curr_preset
