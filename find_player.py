from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class FindPlayer(QMainWindow):
    def __init__(self, session):
        super().__init__()
        uic.loadUi("uis/results_get_player_ui.ui", self)
        self.find_btn.clicked.connect(self.find_player)
        self.session = session
        self.labels = (self.score_label, self.mean_score_label, self.wins_label, self.games_label)

    def find_player(self):
        login = self.player_lne.text()
        for i in self.labels:
            i.clear()
        self.error_label.clear()
        res = self.session.cursor.execute(f"""
            select score, mean_score, wins, games 
            from score
            where id = (select id from users where login = '{login}')
        """).fetchone()
        if not res:
            self.error_label.setText("Данная учётная запись не найдена.")
            res = self.session.cursor.execute(f"""
                select login from users
                where lower(login) = '{login.lower()}'       
            """).fetchone()
            if res:
                self.error_label.setText(
                    "Данная учётная запись не найдена. Может быть вы имели ввиду:\n" + '\n'.join(res))
        else:
            for wid, text in zip(self.labels, res):
                wid.setText(str(text))
