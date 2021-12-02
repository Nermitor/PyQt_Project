from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class GameResults(QMainWindow):
    """Последнее окно, выводит список победителей и их очки"""

    def __init__(self, session):
        super().__init__()
        self.session = session
        uic.loadUi("uis/game_results_ui.ui", self)
        self.load_winners()
        self.exit_btn.clicked.connect(self.close)

        self.setWindowIcon(QIcon("icons/ico.ico"))

    def load_winners(self):
        for login, score in self.session.others['winners']:
            self.listWidget.addItem(f"{login} (+{score})")
