from windows.table import Table
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget
from windows.words_pack_editor import WordsPackEditor

class WordsPackTable(Table):
    """Отображает наборы слов"""
    def __init__(self, session):
        self.query = """
            select pack_name, count(DISTINCT picture_name_id) as c
            from packs inner join words on packs.pack_id = words.pack_id
            where visibility = true
            group by packs.pack_id
        """
        self.vars = {
            0: "\norder by pack_name ASC",
            1: '\norder by c DESC'
        }
        super().__init__(session, "uis/words_packs_table_ui.ui")
        self.tableWidget.itemDoubleClicked.connect(self.edit_pack)
        self.add_btn.clicked.connect(self.add_pack)
        self.refresh_btn.clicked.connect(self.update_table)
        self.delete_pack_btn.clicked.connect(self.delete_pack)

    def edit_pack(self, item: QTableWidgetItem):
        """Вызывает редактирование набора"""
        if item.column() == 1:
            pack_name_row = item.row()
            pack_name = self.tableWidget.item(pack_name_row, 0).text()
            self.editor = WordsPackEditor(self.session, pack_name)
            self.editor.show()

    def add_pack(self):
        """Добавляет новый набор"""
        self.editor = WordsPackEditor(self.session)
        self.editor.show()

    def delete_pack(self):
        """Удаляет набор"""
        items = self.tableWidget.selectedItems()
        rows = set(map(lambda x: x.row(), items))
        packs_names = [self.tableWidget.item(row, 0) for row in rows]
        packs_names = map(lambda x: x.text(), packs_names)
        self.session.cursor.execute(f"""
            update packs
            set visibility = false
            where pack_name in ({','.join(map(lambda x: x.join("''"), packs_names))})
        """)
        self.session.commit()


