from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from windows.painter import Painter
from itertools import chain


class Auth(QMainWindow):
    def __init__(self, session):
        super().__init__()
        uic.loadUi("uis/auth_ui.ui", self)
        self.session = session  # Создание игровой сессии
        self.add_player_btn.clicked.connect(self.add_player)  # Подключение кнопок к функциям
        self.ok_btn.clicked.connect(self.ok)
        self.load_packs()
        self.setWindowIcon(QIcon("icons/ico.ico"))

    def add_player(self):
        """Добавляет игрока к игровой сессии, в случае нового - в базу данных"""
        self.error_label.clear()

        login = self.login_lne.text()
        password = self.password_lne.text()  # Получение логина и пароля из соответствующих полей

        if self.new_player_cb.isChecked():  # Если пользователь хочет создать новую учётку
            if self.check_fields(login, password):  # Если логин и пароль соответствуют правилам
                self.add_player_to_db(login, password)  # Добавление игрока в базу данных
            else:
                return
        self.add_player_to_table(login, password)  # Добавление игрока в игровую сессию

    def check_fields(self, login, password):
        """Проверка полей логина и пароля"""
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
        """Добавляет игрока в базу данных"""
        if len(self.session.cursor.execute(f"""
            select * from users 
            where login = '{login}'
        """).fetchall()) == 0:  # Проверка на существование учётки
            self.session.cursor.execute(f"""
                insert into users (login, password) values('{login}', '{password}')
            """)  # Добавление новой учётки в базу данных
            self.error_label.setText("")
        else:
            self.error_label.setText("Такой пользователь уже есть.")

    def add_player_to_table(self, login, password):
        result = self.session.cursor.execute(f"""
            select * from users where login = '{login}'
        """).fetchall()  # Поиск нужной учётки
        if len(result) == 0:  # Проверка на её существование
            self.error_label.setText("Такой учётной записи не существует.")
        else:
            if str(result[0][1]) != str(password):  # Проверка на соответствие пароля
                self.error_label.setText("Неправильный пароль.")
            else:
                if login in self.session.players:  # Проверка на то, добавлен ли угрок уже или нет
                    self.error_label.setText("Этот игрок уже добавлен.")
                else:
                    self.session.add_player(login)  # Добавление игрока в игровую сессию
                    f = self.session.cursor.execute(f"""
                        select score from score 
                        where id = (select id from users where login = '{login}')
                    """).fetchone()[0]  # Поиск рейтинга нужного игрока
                    self.players_tbl.addItem(f"{login} - {f}")  # Добавление игрока в список игроков
                    self.login_lne.clear()
                    self.password_lne.clear()

    def load_packs(self):
        """Загружает доступные наборы слов в combobox"""
        packs = self.session.cursor.execute(f"""
            select pack_name from packs
            where visibility = true
        """).fetchall()
        self.packs_cb.addItems(map(str, chain(*packs)))

    def ok(self):
        if len(self.session.players) < 2:  # Проверка на достаточное количество игроков
            self.error_label.setText("Для игры требуется как минимум 2 игрока.")
        else:
            self.session.commit()  # Подтверждение изменений в бд
            self.painter = Painter(self.session, self.packs_cb.currentText())
            self.painter.show()  # Вызов следующего окна
            self.close()
