from PyQt5.QtCore import QThread
from flask import Flask
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
class FlaskThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        app = Flask(__name__)

        @app.route('/')
        def hello():
            return 'Hello from Flask!'

        app.run()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initFlask()

    def initUI(self):
        btn = QPushButton('Click me', self)
        btn.clicked.connect(self.buttonClicked)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PyQt5 Web Server Example')

    def initFlask(self):
        self.flask_thread = FlaskThread()
        self.flask_thread.start()

    def buttonClicked(self):
        print('Button Clicked')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
