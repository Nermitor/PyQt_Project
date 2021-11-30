from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from find_player import FindPlayer


class Results(QMainWindow):
    def __init__(self, session):
        super().__init__()
        uic.loadUi("uis/results_ui.ui", self)
        self.find_player_btn.clicked.connect(self.find_player)
        self.get_table_btn.clicked.connect(self.get_table)

        self.session = session


    def find_player(self):
        self.finder = FindPlayer(self.session)
        self.finder.show()

    def get_table(self):
        pass