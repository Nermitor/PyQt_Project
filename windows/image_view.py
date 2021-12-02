from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow


class ImageView(QMainWindow):
    def __init__(self, image):
        super().__init__()
        uic.loadUi("uis/image_view_ui.ui", self)
        self.label.setPixmap(QPixmap(image))
        self.setWindowIcon(QIcon("icons/ico.ico"))
