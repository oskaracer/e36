from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QThread

import sys
from flaskServer import Server
from window import MainWindow
from App import App

class FlaskThread(QThread):
    def __init__(self, backend, ui):
        super().__init__()
        Server.backend = backend
        Server.ui = ui

    def run(self):

        Server.app.run()

# Start UI
app = QApplication(sys.argv)
ui = MainWindow()


backend = App()


# Start server
flask_thread = FlaskThread(backend, ui)
flask_thread.start()


backend.ui = ui
backend.server = Server

ui.backend = backend
ui.server = Server

ui.initUI()
# Start control backend

ui.ledScreen.update_screen()
ui.flapScreen.update_screen()

sys.exit(app.exec_())

