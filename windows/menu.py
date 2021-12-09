from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from session import Session
from windows.auth import Auth
from windows.scores import Scores
from windows.words_packs_table import WordsPackTable


class Menu(QMainWindow):
    """Меню"""
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/menu_ui.ui", self)
        self.session = Session("db.sqlite")
        self.new_game_btn.clicked.connect(self.start_players_window)
        self.results_btn.clicked.connect(self.results)
        self.words_packs_btn.clicked.connect(self.words_packs)
        self.setWindowIcon(QIcon("icons/ico.ico"))

    def start_players_window(self):
        self.players_window = Auth(self.session)
        self.players_window.show()
        self.close()

    def results(self):
        self.res = Scores(self.session)
        self.res.show()

    def words_packs(self):
        self.pack = WordsPackTable(self.session)
        self.pack.show()
