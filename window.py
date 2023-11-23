import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap

from PresetBtn import  PresetButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.backend = None
        self.server = None

    def initUI(self):
        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        self.screen1 = QLabel('Screen 1', alignment=Qt.AlignCenter)
        self.screen1.setPixmap(QPixmap('img/screen_info.jpg'))

        self.ledScreen = LedScreen(self)
        self.flapScreen  = FlapScreen(self)


        self.central_widget.addWidget(self.screen1)
        self.central_widget.addWidget(self.ledScreen.screen)
        self.central_widget.addWidget(self.flapScreen.screen)

        self.current_screen_index = 0
        self.drag_start_position = QPoint()

        self.central_widget.installEventFilter(self)

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Multi-Screen Qt Application')
        self.show()

    def eventFilter(self, obj, event):
        if obj == self.central_widget:
            if event.type() == event.MouseButtonPress and event.buttons() == Qt.LeftButton:
                self.drag_start_position = event.pos()
            elif event.type() == event.MouseMove and event.buttons() == Qt.LeftButton:
                delta = event.pos() - self.drag_start_position
                if delta.manhattanLength() > 20:  # Adjust the sensitivity of the drag
                    self.handleDrag(delta)
                    self.drag_start_position = event.pos()
            elif event.type() == event.MouseButtonRelease and event.buttons() == Qt.LeftButton:
                self.handleDragEnd(event.pos())
        return super().eventFilter(obj, event)

    def handleDrag(self, delta):
        if delta.x() < 0:
            self.showNextScreen()
        elif delta.x() > 0:
            self.showPreviousScreen()

    def handleDragEnd(self, end_pos):
        # Add any additional logic when drag ends (if needed)
        pass

    def showNextScreen(self):
        if self.current_screen_index < self.central_widget.count() - 1:
            self.current_screen_index += 1
            self.central_widget.setCurrentIndex(self.current_screen_index)

    def showPreviousScreen(self):
        if self.current_screen_index > 0:
            self.current_screen_index -= 1
            self.central_widget.setCurrentIndex(self.current_screen_index)


class FlapScreen(object):

    def __init__(self, mainwindow):

        self.parent = mainwindow

        self.screen = QLabel('Screen 3', alignment=Qt.AlignCenter)
        self.screen.setPixmap(QPixmap('img/screen_flap.jpg'))

        self.vLayout = QVBoxLayout(self.screen)  # 3 Rows - text, btn, btn


    def update_screen(self):
        state = self.parent.backend.exhaustFlap.state
        btn = PresetButton(self.screen, screen=self)
        btn.setText("Exhaust Flap")
        self.vLayout.addWidget(btn)

        if state and btn._pressed:
            btn.toggle(True)

    def btn_pressed_cb(self, btn):
        self.parent.backend.exhaustFlap.toggleExhaustFlap()
        print(f"Pressed button: {btn} Exhaust flap. Flap new state: {self.parent.backend.exhaustFlap.state}")

    def toggle_button(self, name):

        for l in range(self.vLayout.count()):
            btn = self.vLayout.itemAt(l)
            if btn and btn.widget():
                btn = btn.widget()
                if btn.text() == name:
                    print(f"Toggle btn {name} from server")
                    btn.toggle(False)
                    return True

        print("Some error, button not found in flap")

class LedScreen(object):

    MAX_PRESETS = 6

    def __init__(self, mainwindow):
        self.parent = mainwindow

        self.screen = QLabel('Screen 2', alignment=Qt.AlignCenter)
        self.screen.setPixmap(QPixmap('img/screen_led_modes.jpg'))

        self.vLayout = QVBoxLayout(self.screen)  # 3 Rows - text, btn, btn
        self.vLayout.setContentsMargins(20, 80, 20, 20)
        self.rowOne = QHBoxLayout(self.screen)
        self.rowTwo = QHBoxLayout(self.screen)
        self.rowThr = QHBoxLayout(self.screen)

        self.vLayout.addLayout(self.rowOne)
        self.vLayout.addLayout(self.rowTwo)
        self.vLayout.addLayout(self.rowThr)


    def update_screen(self):

        sel_presets = self.parent.backend.presets.load_selected_presets()
        all_presets = self.parent.backend.presets.load_last_presets()
        # presets = {} # {all_presets[x] for x in all_presets.keys() if x in sel_presets}
        # for pr in sel_presets:
        #     pr = pr.strip()
        #     if pr in all_presets.keys():
        #         presets.update({pr: all_presets[pr]})
        #
        # if len(presets) > self.MAX_PRESETS:
        #     presets_names = list(presets.keys())[:6]
        # else:
        #     presets_names = presets.keys()

        presets_names = [x.strip() for x in sel_presets if x.strip() in all_presets.keys()]

        print(presets_names)

        for i, pr in enumerate(presets_names):

            btn = PresetButton(self.screen, screen=self)
            btn.setText(str(pr))
            print(pr)
            if i < 3:
                self.rowTwo.addWidget(btn)
            else:
                self.rowThr.addWidget(btn)

    def off_buttons(self, exc):

        for l in range(self.vLayout.count()):
            layout_item = self.vLayout.itemAt(l)
            if layout_item and layout_item.layout():
                hbox = layout_item.layout()
                for i in range(hbox.count()):
                    btn = hbox.itemAt(i)
                    if btn and btn.widget():
                        btn = btn.widget()

                        if btn == exc:
                            continue

                        if btn._pressed:
                            btn.toggle(True)

    def btn_pressed_cb(self, btn):

        print(f"Pressed button: {btn.text()}")
        self.off_buttons(exc=btn)
        if not btn._pressed:
            return self.parent.backend.set_curr_preset(None)
        else:
            return self.parent.backend.set_curr_preset(btn.text())
           # return self.parent.backend.presets.load_preset(btn.text(), self.parent.backend.leds)

    def toggle_button(self, name):

        for l in range(self.vLayout.count()):
            layout_item = self.vLayout.itemAt(l)
            if layout_item and layout_item.layout():
                hbox = layout_item.layout()
                for i in range(hbox.count()):
                    btn = hbox.itemAt(i)
                    if btn and btn.widget():
                        btn = btn.widget()

                        if btn.text() == name:
                            print(f"Toggle btn {name} from server. old state: {btn._pressed}")
                            btn.toggle(False)
                            return True

        print("Button is not active, need to update btns")

        #self.