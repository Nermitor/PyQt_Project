import sys

from PyQt5.QtWidgets import QApplication

from windows.menu import Menu


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = Menu()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
