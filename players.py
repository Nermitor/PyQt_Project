import sqlite3 as sql
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from painter import Painter
from session import Session


class PlayersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/players_ui.ui", self)
        self.session = Session(sql.connect("db.sqlite"))
        self.add_player_btn.clicked.connect(self.add_player)
        self.ok_btn.clicked.connect(self.ok)

    def add_player(self):
        self.error_label.clear()
        login = self.login_lne.text()
        password = self.password_lne.text()
        if self.new_player_cb.isChecked():
            if self.check_fields(login, password):
                self.add_player_to_db(login, password)
            else:
                return
        self.add_player_to_table(login, password)

    def check_fields(self, login, password):
        if login == '':
            self.error_label.setText("Логин не должен быть пустым.")
            return False
        elif password == '':
            self.error_label.setText("Пароль не должен быть пустым.")
            return False
        elif len(password) < 8:
            self.error_label.setText("Длина пароля должна быть больше или равна 8.")
            return False
        elif len(login) < 3:
            self.error_label.setText("Длина логина должна быть больше или равна 3.")
            return False
        return True

    def add_player_to_db(self, login, password):
        if len(self.session.cursor.execute(f"""select * from users where login = '{login}'""").fetchall()) == 0:
            self.session.cursor.execute(f"""
            insert into users (login, password) values('{login}', '{password}')
            """)
            self.error_label.setText("")
        else:
            self.error_label.setText("Такой пользователь уже есть.")

    def add_player_to_table(self, login, password):
        result = self.session.cursor.execute(f"""
        select * from users where login = '{login}'
        """).fetchall()
        if len(result) == 0:
            self.error_label.setText("Такой учётной записи не существует.")
        else:
            if str(result[0][1]) != str(password):
                self.error_label.setText("Неправильный пароль.")
            else:
                if login in self.session.players:
                    self.error_label.setText("Этот игрок уже добавлен.")
                else:
                    f = str(
                        self.session.cursor.execute(f"""
                        select score from score 
                        where id = (select id from users where login = '{login}')
                        """).fetchone()[0])
                    self.players_tbl.addItem(f"{login} - {f}")
                    self.session.add_player(login)

    def ok(self):
        self.session.commit()
        self.painter = Painter(self.session)
        self.painter.show()
        self.close()
