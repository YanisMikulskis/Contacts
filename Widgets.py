import builtins

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QGraphicsOpacityEffect
from PyQt5.QtWidgets import QTableWidget, QWidget, QGridLayout, QTableWidgetItem, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt


# Общие классы
class Window(QMainWindow):  # класс виджета окна
    def __init__(self) -> QMainWindow:
        super(Window, self).__init__()
        self.setWindowTitle('ChatGPT')
        self.setGeometry(300, 250, 600, 500)


class Label:  # класс виджета надписей
    def __init__(self, window: QMainWindow, right: int, down: int, content: str) -> QLabel:
        self.text: QLabel = QLabel(window)
        self.text.setText(content)
        self.text.move(right, down)
        self.text.adjustSize()
        self.text.show()

    def del_widget(self):
        self.text.clear()


class Button:  # класс виджета кнопок
    def __init__(self, window: QMainWindow, content: str, right: int, down: int, size: int) -> QPushButton:
        self.btn: QPushButton = QPushButton(window)  # на этом шаге кнопка появляется
        self.btn.move(right, down)
        self.btn.setText(content)
        self.btn.setFixedWidth(size)
        self.btn.show()

    def click(self, func: object):
        self.btn.clicked.connect(func)

    def del_widget(self):
        self.btn.deleteLater()


class Line:  # класс виджета поля для ввода текста
    def __init__(self, window: QMainWindow, right: int, down: int, size: int):
        self.line: QLineEdit = QLineEdit(window)
        self.line.move(right, down)
        self.line.setFixedWidth(size)

    def del_widget(self):
        self.line.deleteLater()


class Table:  # класс виджета таблицы
    def __init__(self, window: QMainWindow, data: list) -> QTableWidget:
        # Создаем пустой виджет как основу
        self.central_widget: QWidget = QWidget()
        window.setCentralWidget(self.central_widget)
        # Создаем рабочий слой и кидаем его в виджет
        self.table_layout: QGridLayout = QGridLayout()
        self.central_widget.setLayout(self.table_layout)
        # Создаем нашу таблицу
        self.table: QTableWidget = QTableWidget(window)
        self.table.setColumnCount(4)  # количество столбцов
        self.table.setRowCount(len(data))  # количество строк
        self.table.setHorizontalHeaderLabels(
            ['id (в БД)', 'Имя', 'Номер телефона', 'Электронная почта'])  # Названия столбцов
        # ниже выравнивание названий колонн по центру
        [self.table.horizontalHeaderItem(column_number).setTextAlignment(Qt.AlignHCenter) for column_number in range(3)]
        for row in enumerate(data):  # заполнение полей
            self.table.setItem(row[0], 0, QTableWidgetItem(row[1][0]))
            self.table.setItem(row[0], 1, QTableWidgetItem(row[1][1]))
            self.table.setItem(row[0], 2, QTableWidgetItem(row[1][2]))
            self.table.setItem(row[0], 3, QTableWidgetItem(row[1][3]))
        self.table.resizeColumnsToContents()  # Выравнивание столбцов по контенту
        self.table_layout.addWidget(self.table)

    def del_widget(self):
        [widget.deleteLater() for widget in [self.central_widget, self.table_layout, self.table]]


class MessageBox:  # класс виджета всплывающего сообщения
    def __init__(self, content: str, content_button: str, level_message: str) -> QMessageBox:
        self.msg: QMessageBox = QMessageBox()
        self.msg.setText(content)
        levels_message = {
            'Warning': QMessageBox.Warning,
            'Info': QMessageBox.Information,
            'Question': QMessageBox.Question
        }
        self.msg.setIcon(levels_message[level_message])
        if level_message != 'Question':
            self.msg.addButton(content_button, QMessageBox.RejectRole)
        else:
            self.msg.addButton('Да', QMessageBox.AcceptRole)
            self.msg.addButton('Нет', QMessageBox.AcceptRole)

        self.msg.exec_()

    def del_widget(self):
        self.msg.deleteLater()


class CheckBox:  # класс виджета чекбокса - кнопки, которая может быть вкл или выкл.
    def __init__(self, window: QMainWindow, content: str, right: int, down: int) -> QCheckBox:
        self.checkbox: QCheckBox = QCheckBox(window)
        self.checkbox.move(right, down)
        self.checkbox.setText(content)
        self.checkbox.setFixedWidth(150)
        self.content: str = self.checkbox.text()
        self.checkbox.show()

    def del_widget(self):
        self.checkbox.deleteLater()
