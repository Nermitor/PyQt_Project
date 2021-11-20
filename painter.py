from PyQt5 import uic
from random import choice
from PyQt5.QtCore import QSize, QPoint, QTimer, Qt
from PyQt5.QtGui import QColor, QImage, QPainterPath, QPainter, QPen
from PyQt5.QtWidgets import QFrame, QMainWindow, QColorDialog
from votes import Votes


class PaintField(QFrame):
    def __init__(self, width, parent=None):
        super().__init__(parent)
        self.default_color = QColor("black")
        self.default_fill_color = QColor('white')

        self.size = QSize(1051, 591)
        self.pos = QPoint(20, 190)

        self.resize(self.size)
        self.move(self.pos)

        self.width = width

        self.image = QImage(self.size, QImage.Format_RGB32)
        self.reset()

        self.path = QPainterPath()

    def reset(self):
        self.fill(self.default_fill_color)
        self.color = self.default_color
        self.update()

    def save(self, name):
        file_type = name.split('.')[1]
        self.image.save(name, file_type.upper())

    def fill(self, color):
        self.image.fill(color)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.image, self.rect())

    def mousePressEvent(self, event):
        self.path.moveTo(event.pos())

    def mouseMoveEvent(self, event):
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
    def __init__(self, players, connection):
        super().__init__()
        uic.loadUi("uis/painter_ui.ui", self)

        self.connection = connection
        self.cur = self.connection.cursor()

        self.word = self.set_word()
        self.word_lbl.setText(self.word)

        self.plrs = players

        self.players = iter(players)

        self.total_time = 120
        self.estimated_time = self.total_time

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.setInterval(1000)
        self.timer.start()

        self.width_sb.valueChanged.connect(self.set_width)
        self.set_color_btn.clicked.connect(self.set_color)
        self.ok_btn.clicked.connect(self.go_next)
        self.fill_btn.clicked.connect(self.fill)

        self.painter = PaintField(20, self)

        self.width_sb.setValue(self.painter.width)

        self.prepare_for_next_player()

    def set_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.painter.color = color

    def set_width(self, val):
        self.painter.width = val

    def fill(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.painter.fill(color)

    def update_timer(self):
        self.time_lcn.display(self.estimated_time)
        self.estimated_time -= 1
        if self.estimated_time < 0:
            self.go_next()

    def go_next(self):
        self.save_previous()
        self.prepare_for_next_player()

    def prepare_for_next_player(self):
        self.estimated_time = self.total_time
        self.time_lcn.display(self.estimated_time)
        try:
            self.cur_player = next(self.players)
        except StopIteration:
            self.votes = Votes(self.plrs, self.connection)
            self.votes.show()
            self.close()
        self.cur_player_lbl.setText(self.cur_player)
        self.painter.reset()

    def save_previous(self):
        self.painter.save(f"pictures/temp/{self.cur_player}.png")

    def set_word(self):
        words = self.cur.execute("""
        select picture_name from words
        """).fetchall()
        return choice(words)[0]
