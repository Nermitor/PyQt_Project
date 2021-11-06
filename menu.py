from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic


class Menu(QMainWindow):
    def __init__(self, players_window):
        super().__init__()
        uic.loadUi("uis/menu_ui.ui", self)
        self.players_window = players_window
        self.new_game_btn.clicked.connect(self.start_players_window)

    def start_players_window(self):
        self.close()
        self.players_window.show()
