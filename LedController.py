
# Parent is App class (backend)
class LEDController(object):

    animation_descr = {}

    def __init__(self, parent):

        self.parent = parent

    def update_led_state(self):

        pr_descr = self.parent.presets.storage[self.parent.curr_preset]

        for led in pr_descr:

            if "animation" in led.keys() and led['animation'] is not None:
                print("Process animation")
            else:
                print(f"Change static GPIO for LED: {led}")

        return True