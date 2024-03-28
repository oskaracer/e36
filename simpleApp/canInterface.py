import can
import sys
import threading
import os
from datetime import datetime
import time

VCC_MSG_ID = 0x400

class CanInterface(threading.Thread):

    def __init__(self, iface, app):
        super().__init__()

        self.iface_name = iface
        self.bus = can.interface.Bus(channel=self.iface_name, interface="socketcan")

        self.msg_id_filter = [0x400]

        self.logfile = None

        self.app = app

        self.paused = True
        self.done = False

    def set_logfile(self, filename):

        dirs = os.path.dirname(filename)
        os.makedirs(dirs, exist_ok=True) if not dirs == '' else None

        self.logfile = filename

        print("Logfile changed to: {}".format(filename))

    def log(self, msg):

        if self.logfile is None:
            self.set_logfile(datetime.now().strftime("logs/%Y%m%d-%H%M%S.log"))

        print(msg)
        with open(self.logfile, 'a') as f:
            f.write(str(msg) + '\n')

    def run(self):

        print(f"Can Listener of port: {self.iface_name} is starting")

        # Do sth
        while not self.done:

            if self.paused:
                time.sleep(1)
                continue

            msg = self.bus.recv(timeout=1)
            self.log(msg)
            if msg is not None:
                self.process_msg(msg)
            else:
                print(None)

    def stop(self):

        self.done = True
        print(f"Can Listener of port: {self.iface_name} is stopped")

    def start_listener(self):
        self.paused = False
        print("Can Listener started logging")

    def stop_listener(self):
        self.paused = True
        print("Can Listener paused logging")

    def process_msg(self, msg):

        if msg.arbitration_id in self.msg_id_filter:
          #  print(f"MSG: {msg}")

            if self.app is not None:
                if msg.arbitration_id == VCC_MSG_ID:    # TODO: GET REAL PACKET
                    vcc = int(msg.data[0])
                    self.app.on_new_data("VCC", vcc)
                    self.app.on_new_data("FUEL", {"currentFuel": 5, "currentOdo": 10})


if __name__ == "__main__":

    canIface = CanInterface("can0", None)
    canIface.start()
    canIface.join()