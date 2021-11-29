from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class BestPlayers(QMainWindow):
    """Последнее окно, выводит список победителей и их очки"""
    def __init__(self, session):
        super().__init__()
        self.session = session
        uic.loadUi("uis/best_players_ui.ui", self)
        self.load_winners()
        self.exit_btn.clicked.connect(self.close)

    def load_winners(self):
        for login, score in self.session.others['winners']:
            self.listWidget.addItem(f"{login} (+{score})")
