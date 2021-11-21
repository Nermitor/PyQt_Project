from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from funcs import prod
from PyQt5 import uic
from math import ceil
from datetime import datetime
from clean import clean_temp_folder


class Votes(QMainWindow):
    """Окно с оценкой изображений"""

    def __init__(self, session):
        super().__init__()
        uic.loadUi("uis/votes_ui.ui", self)  # Загрузка интерфейса
        self.session = session  # Наследование игровой сессии

        self.score = {i: 0 for i in session.players}  # Словарь игрок - очки
        self.players = prod(session.players)  # Список списков игрок - остальные игроки

        self.winner_bonus = 1.1  # Множитель очков для победившего игрока(ов)

        self.ok_btn.clicked.connect(self.prepare)
        self.go_next()

    def go_next(self):
        """Отображает следующюю пару (голосующий - картинка другого игрока)"""
        try:
            self.voter, self.img = next(self.players)
        except StopIteration:
            self.set_score()
            self.close()
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
        self.set_best_picture(winners)
        clean_temp_folder()
        self.session.commit()

    def set_best_picture(self, winners):
        """Устанавливает результат лучших картинок"""
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

            pic = QPixmap(f"pictures/temp/{login}.png")
            pic.save(self.get_last_path(), "PNG")
        self.session.commit()

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
            if login in winners:  # Прверка на победившего(их) игрока
                score = ceil(score * self.winner_bonus)  # Домножение результата на множитель бонуса
            self.session.cursor.execute(f"""
                update score
                set score = score + {score}
                where id = (select id from users where login = '{login}')
            """)  # Обновление результата всех игроков

    def prepare(self):
        """Сохраняет предыдущее и подготавливает к следующему"""
        self.save_prev()
        self.go_next()
