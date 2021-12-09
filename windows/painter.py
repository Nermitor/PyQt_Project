from random import choice

from PyQt5 import uic
from PyQt5.QtCore import QSize, QPoint, QTimer, Qt
from PyQt5.QtGui import QColor, QImage, QPainterPath, QPainter, QPen, QIcon
from PyQt5.QtWidgets import QFrame, QMainWindow, QColorDialog

from windows.votes import Votes


class PaintField(QFrame):
    """Поле для рисования"""

    def __init__(self, width, parent=None):
        super().__init__(parent)
        self.default_color = QColor("black")
        self.default_fill_color = QColor('white')
        self.size = QSize(1051, 591)
        self.pos = QPoint(20, 190)
        self.resize(self.size)
        self.move(self.pos)
        self.width = width
        self.image = QImage(self.size, QImage.Format_RGB32)  # Инициалиизация основных параметров

        self.reset()
        self.path = QPainterPath()

    def reset(self):
        """Сбрасывает параметры к значениям по умолчанию"""
        self.fill(self.default_fill_color)  # Заливка
        self.color = self.default_color  # Цвет пера
        self.update()

    def save(self, name):
        """Сохраняет изображение в виде файла"""
        file_type = name.split('.')[1]
        self.image.save(name, file_type.upper())

    def fill(self, color):
        """Заливает изображение переданным цветом"""
        self.image.fill(color)

    def paintEvent(self, event):
        """Специальный метод"""
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.image, self.rect())

    def mousePressEvent(self, event):
        """Специальный метод"""
        self.path.moveTo(event.pos())

    def mouseMoveEvent(self, event):
        """Специальный метод"""
        self.path.lineTo(event.pos())
        p = QPainter(self.image)
        p.setPen(QPen(self.color,
                      self.width,
                      Qt.SolidLine, Qt.RoundCap,
                      Qt.RoundJoin))
        p.drawPath(self.path)
        p.end()
        self.update()
        self.path = QPainterPath(event.pos())


class Painter(QMainWindow):
    """Основное окно"""

    def __init__(self, session, pack_name):
        super().__init__()
        uic.loadUi("uis/painter_ui.ui", self)  # Загрузка интерфейса

        self.session = session  # Наследование игровой сессии
        self.pack_name = pack_name
        self.word = self.get_word()  # Установка слова для рисования
        self.session.add_others('key_word', self.word)  # Добавление слова к дополнительным параметрам игровой сессии
        self.word_lbl.setText(self.word)  # Выведение вышеупомянутого слова на экран
        self.players = iter(self.session.players)

        self.total_time = 120  # Общее время для рисоывания
        self.estimated_time = self.total_time  # Текущее оставшееся время


        self.timer = QTimer(self)  # Таймер для обновления времени
        self.timer.timeout.connect(self.update_timer)
        self.timer.setInterval(1000)  # Установка интервала таймера в 1 секунду
        self.timer.start()

        self.width_sb.valueChanged.connect(self.set_width)
        self.set_color_btn.clicked.connect(self.set_color)
        self.ok_btn.clicked.connect(self.go_next)
        self.fill_btn.clicked.connect(self.fill)  # Подключение кнопок к функциям

        self.painter = PaintField(20, self)  # Инициализация поля для рисования

        self.width_sb.setValue(self.painter.width)

        self.setWindowIcon(QIcon("icons/ico.ico"))

        self.prepare_for_next_player()

    def set_color(self):
        """Устанавливает цвет выбранный в диалоге выбора цвета перу"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.painter.color = color

    def set_width(self, val):
        """Устанавливает толщину пера """
        self.painter.width = val

    def fill(self):
        """Заливает поле для рисования"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.painter.fill(color)

    def update_timer(self):
        """Обновляет таймер"""
        self.time_lcn.display(self.estimated_time)
        self.estimated_time -= 1
        if self.estimated_time < 0:
            self.go_next()

    def go_next(self):
        self.save_previous()
        self.prepare_for_next_player()

    def prepare_for_next_player(self):
        """Подготавлявает поле для рисования и окно к следующему игроку"""
        self.estimated_time = self.total_time  # Изначально оставшееся время равно максимальному
        self.time_lcn.display(self.estimated_time)  # Вывод времени на экран
        try:
            self.cur_player = next(self.players)
        except StopIteration:  # Когда кончились игрока
            self.votes = Votes(self.session)
            self.votes.show()
            self.close()
        self.cur_player_lbl.setText(self.cur_player)  # Вывод логина следующего игрока на экран
        self.painter.reset()  # Сброс окна рисования

    def save_previous(self):
        """Сохраняет поле для рисования в виде картинки"""
        self.painter.save(f"pictures/temp/{self.cur_player}.png")

    def get_word(self):
        """Выбирает рандомное слово из бд words"""
        words = self.session.cursor.execute(f"""
            select picture_name from words
            where pack_id = (select pack_id from packs where pack_name = '{self.pack_name}' and visibility = true)
        """).fetchall()
        return choice(words)[0]
