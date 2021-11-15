import sys
from PyQt5.QtWidgets import QApplication
from menu import Menu


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = Menu()
    ex.show()
    sys.exit(app.exec())
