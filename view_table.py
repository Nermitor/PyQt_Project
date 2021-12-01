from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic


class ViewTable(QMainWindow):
    def __init__(self, session):
        super().__init__()
        uic.loadUi("uis/table_view_ui.ui", self)
        self.session = session
        self.query = """select login, score, mean_score, games, wins
                        from score inner join users
                        on score.id = users.id"""
        self.update_table()

    def update_table(self, order_by=''):
        result = self.session.cursor.execute(self.query + order_by).fetchall()
        rows_count = len(result)
        column_count = len(result[0])
        self.tableWidget.setRowCount(rows_count)
        for values, row in zip(result, range(rows_count)):
            for i, cell in zip(range(column_count), values):
                self.tableWidget.setItem(row, i, QTableWidgetItem(str(cell)))
