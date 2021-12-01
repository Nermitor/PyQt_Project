from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from players import PlayersWindow
from results import Results
from session import Session


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/menu_ui.ui", self)
        self.session = Session("db.sqlite")
        self.new_game_btn.clicked.connect(self.start_players_window)
        self.results_btn.clicked.connect(self.results)

    def start_players_window(self):
        self.players_window = PlayersWindow(self.session)
        self.players_window.show()
        self.close()

    def results(self):
        self.res = Results(self.session)
        self.res.show()
