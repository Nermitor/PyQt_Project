from PyQt5.QtWidgets import QTableWidgetItem

from windows.image_view import ImageView
from windows.table import Table


class PicturesTable(Table):
    """Окно с рейтингом картинок"""

    def __init__(self, session):
        self.vars = {
            0: "\norder by login ASC",
            1: "\norder by picture_name ASC",
            2: "\norder by path ASC",
            3: "\norder by time DESC",
        }  # Словарь номеров вариантов в комбо-боксе и подходящая сортировка
        self.query = """
            select login, picture_name, path, time
            from best_pictures
            inner join words
            on words.picture_name_id = best_pictures.picture_name_id
            inner join users
            on best_pictures.user_id = users.id
            """  # Стандартное тело запроса
        super().__init__(session, "uis/pictures_table_ui.ui")
        self.tableWidget.itemDoubleClicked.connect(self.present_image)

    def present_image(self, item: QTableWidgetItem):
        if item.column() == 2:
            path = item.text()
            self.image_view = ImageView(path)
            self.image_view.show()
