from datetime import datetime
from math import ceil

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow

from clean import clean_temp_folder
from windows.game_results import GameResults


class Votes(QMainWindow):
    """Окно с оценкой изображений"""

    def __init__(self, session):
        super().__init__()
        uic.loadUi("uis/votes_ui.ui", self)  # Загрузка интерфейса
        self.session = session  # Наследование игровой сессии

        self.score = {i: 0 for i in session.players}  # Словарь игрок - очки
        self.players = self.prod(session.players)  # Список списков игрок - остальные игроки

        self.winner_bonus = 1.1  # Множитель очков для победившего игрока(ов)

        self.setWindowIcon(QIcon("icons/ico.ico"))

        self.ok_btn.clicked.connect(self.prepare)
        self.go_next()

    def go_next(self):
        """Отображает следующую пару (голосующий - картинка другого игрока)"""
        try:
            self.voter, self.img = next(self.players)
        except StopIteration:
            self.set_score()
            self.close()
            self.best_players = GameResults(self.session)
            self.best_players.show()
        self.cur_player_lbl.setText(self.voter)
        self.label.setPixmap(QPixmap(f"pictures/temp/{self.img}.png"))

    def save_prev(self):
        """Сохранение результата игрока в словарь"""
        self.score[self.img] += int(self.score_cb.text())

    def set_score(self):
        """Устанавливает результат в бд"""
        mx = max(self.score.values())
        winners = [i[0] for i in self.score.items() if i[1] == mx]
        self.set_points(winners)
        self.set_best(winners)
        clean_temp_folder()

    def set_best(self, winners):
        """Устанавливает результат лучших игроков"""
        picture_name_id = self.session.cursor.execute(f"""
            select picture_name_id from words
            where picture_name = '{self.session.others['key_word']}'
        """).fetchone()[0]  # Получает id слова для рисования
        time = datetime.now()  # Получение текущих даты и времени
        for user_id, login in self.get_winners_from_db(winners):  # Перебор логина и id победивших игроков
            self.session.cursor.execute(f"""
                insert into best_pictures (user_id, picture_name_id, time)
                values ({user_id}, {picture_name_id}, '{time}')
            """)  # Добавление изображения в бд
            self.session.commit()

            pic = QPixmap(f"pictures/temp/{login}.png")
            pic.save(self.get_last_path(), "PNG")

            self.session.cursor.execute(f"""
                update score
                set wins = wins + 1
                where id = {user_id}
            """)
            self.session.commit()
            # Обновление количества побед для победителей

    def get_last_path(self):
        """Возвращает путь последней картинки"""
        return self.session.cursor.execute(f"""
            select path from best_pictures
            where picture_id = (select max(picture_id) from best_pictures)
        """).fetchone()[0]

    def get_winners_from_db(self, winners):
        """Получает массив логинов и id победивших игроков"""
        return self.session.cursor.execute(f"""
            select id, login from users
            where login in ({', '.join([i.join("''") for i in winners])})
        """).fetchall()

    def set_points(self, winners):
        """Устанавливает результат очков"""
        for login, score in self.score.items():  # Перебор логина и очков всех игроков
            scr = score
            if login in winners:  # Проверка на победившего(их) игрока
                score = ceil(score * self.winner_bonus)  # Умножение результата на множитель бонуса
                scr = f"{score} (+{int((self.winner_bonus - 1) * 100)}%)"
            if self.session.others.get("winners", None) is None:
                self.session.add_others('winners', [(login, scr)])
            else:
                self.session.edit_others('winners', list.append, (login, scr))
            self.session.cursor.execute(f"""
                update score
                set 
                score = score + {score},
                games = games + 1    
                where id = (select id from users where login = '{login}')
            """)
            self.session.commit()
            # Обновление результата всех игроков

    @staticmethod
    def prod(g):
        return iter(sorted([(el1, el) for el1 in g for el in g if el1 != el], key=lambda x: x[0]))

    def prepare(self):
        """Сохраняет предыдущее и подготавливает к следующему"""
        self.save_prev()
        self.go_next()
