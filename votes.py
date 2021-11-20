from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from funcs import prod
from PyQt5 import uic
from math import ceil
import datetime


class Votes(QMainWindow):
    def __init__(self, session):
        super().__init__()
        uic.loadUi("uis/votes_ui.ui", self)
        self.session = session

        self.score = {i: 0 for i in session.players}
        self.players = prod(session.players)

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
        self.set_points(winners)
        self.set_best_picture(winners)

        self.session.commit()

    def set_best_picture(self, winners):
        picture_name_id = self.session.cursor.execute(f"""
        select picture_name_id from words where picture_name = '{self.session.others['key_word']}'
        """).fetchone()[0]
        time = datetime.datetime.now()
        for user_id, login in self.session.cursor.execute(f"""
            select id, login from users
            where login in ({', '.join([i.join("''") for i in winners])})
        """).fetchall():
            cur_pic_id = self.get_next_id()
            self.session.cursor.execute(f"""
            insert into best_pictures (user_id, picture_name_id, time)
            values ({user_id}, {picture_name_id}, '{time}')
            """)

            pic = QPixmap(f"pictures/temp/{login}.png")
            pic.save(f"pictures/best/{cur_pic_id}.png", "PNG")
        self.session.commit()

    def get_next_id(self):
        k = self.session.cursor.execute(f"""
                select max(picture_id) from best_pictures
                """).fetchone()[0]
        return 1 if k is None else k + 1

    @staticmethod
    def get_path_from_id(pic_id):
        return f"pictures/best/{pic_id}.png"

    def set_points(self, winners):
        for login, score in self.score.items():
            if login in winners:
                score = ceil(score * self.winner_bonus)
            self.session.cursor.execute(f"""
            update score
            set score = score + {score}
            where id = (select id from users where login = '{login}')
            """)

    def prepare(self):
        self.save_prev()
        self.go_next()
