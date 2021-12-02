from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Table(QMainWindow):
    """Абстрактный класс для наследования таблиц игроков и картинок"""

    def __init__(self, session, ui_file):
        super().__init__()
        uic.loadUi(ui_file, self)
        self.session = session
        self.ord_by_cmbx.activated.connect(self.update_table)  # Подключение нужной функции к комбо-боксу
        self.update_table(0)
        self.setWindowIcon(QIcon("icons/ico.ico"))

    def update_table(self, order_by):
        result = self.session.cursor.execute(self.query + self.vars[order_by]).fetchall()  # Получение всей таблицы
        if result:
            rows_count = len(result)  # Количество строк
            column_count = len(result[0])  # Количество столбцов
            self.tableWidget.setRowCount(rows_count)
            for values, row in zip(result, range(rows_count)):  # Перебор результата sql-запроса
                for i, cell in zip(range(column_count), values):  # Пееребор нужных ячеек в строке QTableWidget
                    self.tableWidget.setItem(row, i,
                                             QTableWidgetItem(str(cell)))  # Установка нужных значений в нужную ячейку
