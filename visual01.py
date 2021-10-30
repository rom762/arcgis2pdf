from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class MainWindow(QMainWindow): # главное окно
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Hello, world") # заголовок окна
        # положение окна
        self.move(400, 400)

        # размер окна
        self.resize(600, 400)

        self.lbl = QLabel('Hello, world!!!', self)
        self.lbl.move(10, 30)
        # self.lbl.setStyleSheet("border: 1px solid black;")
        self.lbl.adjustSize()

        # creating a label widget
        # self.label_2 = QLabel("====== Adjusted label =====", self)
        self.label_2 = QLabel("Hello, world!!!", self)

        # moving position
        self.label_2.move(10, 100)
        # setting up border
        self.label_2.setStyleSheet("border: 1px solid black;")
        # adjusting the size of label
        # self.label_2.adjustSize()


        # создаём объект шрифта
        self.font = QFont()
        self.font.setFamily("Rubik") # название шрифта
        self.font.setPointSize(12) # размер шрифта
        self.font.setUnderline(True) # подчёркивание
        self.lbl.setFont(self.font) # задаём шрифт метке
        self.lbl.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
