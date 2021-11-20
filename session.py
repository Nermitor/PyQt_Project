class Session:
    def __init__(self, connection, players=None):
        if players is None:
            players = []
        self._players = players
        self._connection = connection

    @property
    def players(self):
        return self._players

    @property
    def cursor(self):
        return self._connection.cursor()

    @property
    def connection(self):
        return self._connection

    def add_player(self, player):
        self._players.append(player)
