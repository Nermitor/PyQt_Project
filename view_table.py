from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class ViewTable(QMainWindow):
    """Выводит результаты игроков в виде таблицы"""
    def __init__(self, session):
        super().__init__()
        uic.loadUi("uis/table_view_ui.ui", self)  # Загрузка интерфейса
        self.session = session  # Установление текущей сессии
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
        self.ord_by_cmbx.activated.connect(self.update_table)  # Подключение нужной функции к комбо-боксу
        self.update_table(0)  # Первичное обновление таблицы

    def update_table(self, order_by):
        result = self.session.cursor.execute(self.query + self.vars[order_by]).fetchall()  # Получение всей таблицы
        rows_count = len(result)  # Количество строк
        column_count = len(result[0])  # Количество столбцов
        self.tableWidget.setRowCount(rows_count)
        for values, row in zip(result, range(rows_count)):  # Перебор результата sql-запроса
            for i, cell in zip(range(column_count), values):  # Пееребор нужных ячеек в строке QTableWidget
                self.tableWidget.setItem(row, i,
                                         QTableWidgetItem(str(cell)))  # Установка нужных значений в нужную ячейку
