from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from players import PlayersWindow


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/menu_ui.ui", self)

        self.new_game_btn.clicked.connect(self.start_players_window)

    def start_players_window(self):
        self.players_window = PlayersWindow()
        self.players_window.show()
        self.close()
