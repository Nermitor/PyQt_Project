from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5.QtGui import QPixmap
from funcs import prod
from PyQt5 import uic


class Votes(QMainWindow):
    def __init__(self, players):
        super().__init__()
        uic.loadUi("uis/votes_ui.ui", self)
        self.plrs = players
        self.score = {i: 0 for i in players}
        self.players = prod(players)
        self.ok_btn.clicked.connect(self.prepare)
        self.go_next()

    def go_next(self):
        try:
            self.voter, self.img = next(self.players)
        except StopIteration:
            print(self.score)
            self.close()
        self.cur_player_lbl.setText(self.voter)
        self.label.setPixmap(QPixmap(f"pictures/temp/{self.img}.png"))

    def save_prev(self):
        self.score[self.img] += int(self.score_cb.text())

    def prepare(self):
        self.save_prev()
        self.go_next()
