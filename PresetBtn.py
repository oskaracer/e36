from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class PresetButton(QPushButton):

    def __init__(self, parent=None, screen=None, size=(96, 60)):
        super().__init__(parent)
        self.screen = screen
        # Set the default size of the button
        self.setFixedSize(size[0], size[1])

        # Custom property to act as a checkbox
        self._pressed = False

        # Connect the clicked signal to the toggle method
        self.clicked.connect(self.toggle)

        # Set the initial state
        self.update_style()

    def __str__(self):

        return f"Button {self.text()}"

    @property
    def pressed(self):
        return self._pressed

    @pressed.setter
    def pressed(self, value):

        if self._pressed != value:
            self._pressed = value

    def toggle(self, skip=False):
        # Toggle the state when the button is clicked
        self.pressed = not self.pressed
        self.update_style()

        # Skip if not need  to take actions, if just need to unpress for example
        if not skip:
            self.screen.btn_pressed_cb(self)


    def update_style(self):
        # Update the button's style based on its state
        color = QColor(255, 128, 0) if self.pressed else QColor(0, 0, 0)
        self.setStyleSheet(
            f"QPushButton {{ background-color: {color.name()}; color: white; border: 4px solid {QColor(255, 128, 0).name()}; }}"
            f"QPushButton:hover {{ background-color: {color.lighter(125).name()}; }}"
            f"QPushButton:pressed {{ background-color: {color.darker(125).name()}; }}"
        )