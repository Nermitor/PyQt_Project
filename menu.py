from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from players import PlayersWindow
from session import Session
from results import Results


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
