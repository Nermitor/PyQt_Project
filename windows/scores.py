from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from windows.find_player import FindPlayer
from windows.pictures_table import PicturesTable
from windows.players_table import PlayersTable


class Scores(QMainWindow):
    """Промежуточное диалоговое окно"""

    def __init__(self, session):
        super().__init__()
        uic.loadUi("uis/scores.ui", self)  # Загрузка интерфейсп
        self.find_player_btn.clicked.connect(self.find_player)
        self.get_picture_table_btn.clicked.connect(self.get_pictures_table)
        self.get_table_btn.clicked.connect(self.get_players_table)  # Подключение кнопок к функциям
        self.session = session
        self.setWindowIcon(QIcon("icons/ico.ico"))

    def find_player(self):
        """Кнопка поиска конкретного игрока"""
        self.finder = FindPlayer(self.session)
        self.finder.show()

    def get_players_table(self):
        """Кнопка вывода общей таблицы"""
        self.players_table = PlayersTable(self.session)
        self.players_table.show()

    def get_pictures_table(self):
        self.pictures_table = PicturesTable(self.session)
        self.pictures_table.show()
