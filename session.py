class Session:
    def __init__(self, connection, players=None, **others):
        if players is None:
            players = []
        self._players = players
        self._connection = connection
        self._others = others

    @property
    def players(self):
        return self._players

    @property
    def cursor(self):
        return self._connection.cursor()

    @property
    def connection(self):
        return self._connection

    @property
    def others(self):
        return self._others

    def get_others(self, key):
        return self._others[key]

    def commit(self):
        self._connection.commit()

    def add_player(self, player):
        self._players.append(player)

    def add_others(self, key, value):
        self._others[key] = value

