import sqlite3 as sql


class Session:
    """Игровая сессия"""

    def __init__(self, connection, players=None, **others):
        if players is None:
            players = []
        self._players = players  # Игроки ниходящиеся в сессии
        self._connection = sql.connect(connection)  # Соединение с бд
        self._cursor = self._connection.cursor()  # Курсор бд
        self._others = others  # Остальные параметры

    @property
    def players(self):
        return self._players

    @property
    def cursor(self):
        return self._cursor

    @property
    def connection(self):
        return self._connection

    @property
    def others(self):
        return self._others

    def commit(self):
        """Подтверждает изменения бд"""
        self._connection.commit()

    def add_player(self, player):
        """Добавляет игроков в сессию"""
        self._players.append(player)

    def add_others(self, key, value):
        """Добавляет новый параметр в сессию"""
        self._others[key] = value

    def edit_others(self, key, method, value):
        method(self._others[key], value)
