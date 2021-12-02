from windows.table import Table


class PlayersTable(Table):
    """Выводит результаты игроков в виде таблицы"""

    def __init__(self, session):
        self.vars = {
            0: "\norder by login ASC",
            1: "\norder by score DESC",
            2: "\norder by mean_score DESC",
            3: "\norder by games DESC",
            4: "\norder by wins DESC",
        }  # Словарь номеров вариантов в комбо-боксе и подходящая сортировка
        self.query = """
            select login, score, mean_score, games, wins
            from score inner join users
            on score.id = users.id
            """  # Стандартное тело запроса
        super().__init__(session, "uis/players_table_ui.ui")
