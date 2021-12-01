from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class FindPlayer(QMainWindow):
    """Ищет конкретного игрока в бд"""
    def __init__(self, session):
        super().__init__()
        uic.loadUi("uis/results_get_player_ui.ui", self)
        self.find_btn.clicked.connect(self.find_player)
        self.session = session
        self.labels = (self.score_label, self.mean_score_label, self.wins_label, self.games_label)

    def find_player(self):
        """Находит нужного игрока"""
        login = self.player_lne.text()  # Получение логина
        for i in self.labels:
            i.clear()  # Обнуление предыдущего результата
        self.error_label.clear()  # Обнуление ошибок
        res = self.session.cursor.execute(f"""
            select score, mean_score, wins, games 
            from score
            where id = (select id from users where login = '{login}')
        """).fetchone()  # Ролучение результата поиска
        if not res:  # Если не нашлось
            self.error_label.setText("Данная учётная запись не найдена.")  # Вывод ошибки на экран
            res = self.session.cursor.execute(f"""
                select login from users
                where lower(login) = '{login.lower()}'       
            """).fetchone()  # Поиск похожих имён
            if res:
                self.error_label.setText(
                    "Данная учётная запись не найдена. Может быть вы имели ввиду:\n" + '\n'.join(res))  # Возможные варианты
        else:  # При успехе
            for wid, text in zip(self.labels, res):
                wid.setText(str(text))  # Вывод данных в соответствующие поля
