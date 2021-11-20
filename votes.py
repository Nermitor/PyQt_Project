from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from funcs import prod
from PyQt5 import uic
from math import ceil


class Votes(QMainWindow):
    def __init__(self, players, connection):
        super().__init__()
        uic.loadUi("uis/votes_ui.ui", self)
        self.connection = connection
        self.cur = connection.cursor()

        self.plrs = players
        self.score = {i: 0 for i in players}
        self.players = prod(players)

        self.winner_bonus = 1.1

        self.ok_btn.clicked.connect(self.prepare)
        self.go_next()

    def go_next(self):
        try:
            self.voter, self.img = next(self.players)
        except StopIteration:
            self.set_score()
            self.close()
        self.cur_player_lbl.setText(self.voter)
        self.label.setPixmap(QPixmap(f"pictures/temp/{self.img}.png"))

    def save_prev(self):
        self.score[self.img] += int(self.score_cb.text())

    def set_score(self):
        mx = max(self.score.values())
        winners = [i[0] for i in self.score.items() if i[1] == mx]
        for login, score in self.score.items():
            if login in winners:
                score = ceil(score * self.winner_bonus)
            self.cur.execute(f"""
            update score
            set score = score + {score}
            where id = (select id from users where login = '{login}')
            """)
        self.connection.commit()

    def prepare(self):
        self.save_prev()
        self.go_next()
