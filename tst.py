import sys
import time
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class WorkerThread(QThread):
    # Define a signal to notify the main thread
    update_signal = pyqtSignal(str)

    def run(self):
        for i in range(5):
            time.sleep(1)
            # Emit the signal with a message
            self.update_signal.emit(f"Update from worker thread: {i+1}")
        self.update_signal.emit("Worker thread finished.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.button = QPushButton("Start Worker Thread")
        self.label = QPushButton("Label for updates")

        # Connect button click to start the worker thread
        self.button.clicked.connect(self.start_worker_thread)

        # Add widgets to the layout
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)

        # Set the central widget
        self.setCentralWidget(self.central_widget)

    def start_worker_thread(self):
        # Create and start the worker thread
        self.worker_thread = WorkerThread()
        self.worker_thread.update_signal.connect(self.update_label)  # Connect the signal to the slot
        self.worker_thread.start()

    def update_label(self, message):
        # Slot to update the label in the main thread
        self.label.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
