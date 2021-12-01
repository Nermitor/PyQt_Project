from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from find_player import FindPlayer
from view_table import ViewTable


class Results(QMainWindow):
    """Промежуточное диалоговое окно"""

    def __init__(self, session):
        super().__init__()
        uic.loadUi("uis/results_ui.ui", self)  # Загрузка интерфейсп
        self.find_player_btn.clicked.connect(self.find_player)
        self.get_table_btn.clicked.connect(self.get_table)  # Подключение кнопок к функциям
        self.session = session

    def find_player(self):
        """Кнопка поиска конкретного игрока"""
        self.finder = FindPlayer(self.session)
        self.finder.show()

    def get_table(self):
        """Кнопка вывода общей таблицы"""
        self.table = ViewTable(self.session)
        self.table.show()
