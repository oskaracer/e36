import time
import threading

has_lib = False
try:
    from neopixel import *
    has_lib = True
except Exception as e:
    print(str(e))
# pip3 install rpi_ws281x adafruit-circuitpython-neopixel

# Parent is App class (backend)
class LEDController(object):
    # LED strip configuration:

    def __init__(self, parent, animationStorage):
        self.animationStorage = animationStorage
        self.led = parent

        # LED strip configuration:
        self.led_count = 10                     # Number of LED pixels.
        self.pin = 18                           # GPIO pin connected to the pixels (18 uses PWM).
        self.freq_hz = 800000                   # LED signal frequency in hertz (usually 800khz)
        self.dma_ch = 10                        # DMA channel to use for generating signal (try 10)
        self.brightness = self.led.brightness   # Set to 0 for darkest and 255 for brightest
        self.inverted = False                   # True to invert the signal (when using NPN transistor level shift)
        self.channel = 0                        # set to '1' for GPIOs 13, 19, 41, 45, 53

        self.anim_thread = None

        if has_lib:
            # Create NeoPixel object with appropriate configuration.
            self.strip = Adafruit_NeoPixel(self.led_count,
                                           self.pin,
                                           self.freq_hz,
                                           self.dma_ch,
                                           self.inverted,
                                           self.brightness,
                                           self.channel)
            self.strip.begin()

    def start_animation(self):
        print(f"Process {self.led.animation} animation: {animation_descr} for {self.led.name} LED")
        while True:
            time.sleep(1)
            print(f"Animating LED: {self.led.name}")

    def update_led_state(self):

        if self.led.animation is not None and self.led.animation != "static":
            animation_descr = self.animationStorage.storage[self.led.animation]
            if has_lib:
                self.anim_thread = threading.Thread(target=self.start_animation)
                self.anim_thread.start()
        else:
            print(f"Change static GPIO for LED: {self.led.name}")
            if has_lib:
                for i in range(self.strip.numPixels()):
                    strip.setPixelColor(i, self.led.color)
                    strip.show()
                    time.sleep(wait_ms / 1000.0)    # IDK WHY X/1000 not X
        return True