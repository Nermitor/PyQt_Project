from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog


class WordsPackEditor(QMainWindow):
    """окно редактирования/добавления наборов слов"""

    def __init__(self, session, edit_pack_name=None):
        super().__init__()
        uic.loadUi("uis/words_pack_editor_ui.ui", self)
        self.session = session
        self.edit_pack_name = edit_pack_name  # В случае редактировния, а не добавления хранится изначально имя
        self.save_pack_btn.clicked.connect(self.save_pack)
        self.load_from_file_btn.clicked.connect(self.set_words_from_file)

        if edit_pack_name:  # При редактировании
            self.set_words_from_pack_name(edit_pack_name)
            self.pack_name_lne.setText(edit_pack_name)

    def set_words_from_pack_name(self, pack_name):
        """Загрузка слов по названию набора"""
        res = self.session.cursor.execute(f"""
            select
            picture_name from words
            where pack_id = (select pack_id from packs where pack_name = '{pack_name}' and visibility = true)
        """).fetchall()
        for word in res:
            self.words_te.appendPlainText(str(word[0]))

    def set_words_from_file(self):
        """Загрузка слов из файла"""
        file_name = QFileDialog.getOpenFileName(self, 'Выбрать файл', 'C:/')[0]
        if self.copy_name_ckb.isChecked():
            title = file_name.split("/")[-1].split('.')[-2]
            self.pack_name_lne.setText(title)
        try:
            with open(file_name, encoding='utf-8') as file:
                for line in file.readlines():
                    self.words_te.appendPlainText(line.strip())
        except Exception:
            self.error_label.setText("Ошибка чтения файла")

    def save_pack(self):
        """Сохранение набора"""
        self.error_label.setText("")
        to_save_words = self.words_te.toPlainText()  # Получение слов из поля
        if to_save_words == '':  # Если поле пустое
            self.error_label.setText("Введите хотя бы одно слово.")
            return
        to_save_words = map(lambda x: (x,), to_save_words.split("\n"))
        pack_name = self.pack_name_lne.text()  # Получение названия набора
        if not pack_name:
            self.error_label.setText("Название набора не должно быть пустым.")
            return
        if self.edit_pack_name is not None:  # Если набор редактируется
            self.session.cursor.execute(f"""
                update packs
                set visibility = FALSE
                where pack_name = '{self.edit_pack_name}'
            """)  # Скрытие слов прошлого набора
            self.session.commit()
        self.session.cursor.execute(f"""
            insert into packs(pack_name) values('{pack_name}')
        """)  # Добавление в бд наборов нового набора
        self.session.commit()
        self.session.cursor.executemany(f"""
            insert into words(picture_name, pack_id)
            values (?, (select max(pack_id) from packs))
        """, to_save_words)  # Доваление в бд слов нове слова
        self.session.commit()
        self.close()
