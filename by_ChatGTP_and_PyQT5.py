# Конечно! Вот сложное задание на Python для вас:
# Задание: Внедрение системы управления контактами.
# Создайте систему управления контактами на основе командной строки с помощью Python. Система должна позволять
# пользователям выполнять следующие операции:
# Добавить контакт: Пользователи должны иметь возможность добавить новый контакт с такими данными, как имя,
# номер телефона и адрес электронной почты.
# Поиск контакта: Пользователи должны иметь возможность искать контакт по имени и получать его данные.
# Обновить контакт: Пользователи должны иметь возможность обновить данные существующего контакта.
# Удалить контакт: Пользователи должны иметь возможность удалить контакт.
# Список всех контактов: Пользователи должны иметь возможность просматривать все контакты, хранящиеся в системе.
# Сохранить контакты в файл: Контакты должны быть сохранены в файле, чтобы их можно было восстановить позже даже после
# закрытия программы.
# Загрузить контакты из файла: При запуске программы она должна загрузить ранее сохраненные контакты из файла.
# Обработка ошибок: Внедрите надлежащую обработку ошибок для таких случаев, как недопустимый ввод, контакт не найден
# и т. д.
# Необязательные задачи:
# Внедрить проверку номеров телефонов и адресов электронной почты.
# Добавьте функционал искать контакты по номеру телефона или адресу электронной почты.
# Создайте простой графический интерфейс с помощью Tkinter или PyQt для лучшего пользовательского интерфейса.
# Разрешить пользователям экспортировать контакты в различные форматы, такие как CSV или JSON.
# Это задание проверит ваши навыки обработки данных, ввода-вывода файлов, обработки пользовательского ввода и управления
# ошибками в Python. Не стесняйтесь расширять или изменять требования в соответствии с вашими предпочтениями. Удачи!

# В коде имеются некоторые комментарии для облегчения понимания и восприятия. Более подробные и глубокие пояснения о
# работе программы см. в приложенном файле README.md. Основные блоки кода (функции и методы) разделены пунктиром
# для удобного восприятия
import random
import sqlite3
import sys
import yaml
from yaml.loader import FullLoader
import re
from faker import Faker

from Widgets import Window, Label, Button, Line, Table, MessageBox, CheckBox
from PyQt5.QtWidgets import QApplication, QTableWidget, QWidget, QMessageBox, QLabel, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from typing import Callable

app = QApplication(sys.argv)


class DATABASE_PyQT5:  # класс БД
    def __init__(self, name_database: str):
        self.name_database: str = name_database
        self.connection = sqlite3.connect(self.name_database)
        self.cursor = self.connection.cursor()

    def create_table(self):  # создание таблицы
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Contacts_list
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(30) NOT NULL,
            number_phone INTEGER(11) NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
            );
            '''
        )


# -----------------------
db_cont = DATABASE_PyQT5('contacts_pyqt5')
db_cont.create_table()
window = Window()
commands = {
    1: 'Добавить контакт',
    2: 'Поиск контакта по имени',
    3: 'Поиск контакта по почте или телефону',
    4: 'Обновить данные контакта',
    5: 'Удалить контакт по его id',
    6: 'Записать в файл формата YAML',
    7: 'Выгрузить из файла формата YAML',
    8: 'Очистить таблицу',
    9: 'Добавить случайные данные (исп. Faker)',
    10: 'Показать базу данных',
    0: 'Выйти'
}  # Названия кнопок главного меню


# -----------------------
class App:  # главный класс приложения
    def __init__(self):
        self.lines: list = None  # атрибут для временного списка полей ввода
        self.temporary: list = None  # атрибут для временного списка виджетов
        self.mail_line: QLineEdit = None  # атрибут для поля ввода почты
        self.name_line: QLineEdit = None  # атрибут для поля ввода имени
        self.number_line: QLineEdit = None  # атрибут для поля ввода номера
        self.id_line: QLineEdit = None  # атрибут для поля ввода id
        self.line: QLineEdit = None  # атрибут для поля ввода id
        self.widgets_collection: list = []
        # self.widgets_collection - коллекция всех виджетов текущей страницы. Нужна, чтобы при переходе на другую
        # страницу экран очищался за счет манипуляций с данной коллекцией, а после коллекция будет заполняться
        # новыми виджетами (т.е. виджетами страницы, на которую мы перешли)
        self.label_method(right=240, down=50, content='Здравствуйте')  # создание виджета текста
        self.button_method(content=f'Начать', right=150, down=75, size=300, func=self.page_commands)
        # коллекция методов для работы с БД
        self.database_methods: dict = {
            1: self.page_insert,
            2: self.page_search_name,
            3: self.page_search_number_mail,
            4: self.page_update,
            5: self.del_page,
            6: self.record_yaml_page,
            7: self.load_from_yaml,
            8: self.clear_table,
            9: self.random_values,
            10: self.view_page,
            0: lambda: exit()  # вызов функции выхода из цикла в анонимной функции лямбда
        }

    # Статичные методы для манипуляций с данными
    # -------------------------------------------

    @staticmethod
    def patterns(data: str, meta: str) -> bool:
        """
        Стат. метод для проверки введенных (или измененных) значений для телефона и почты
        """
        if data == 'inp_num':
            if meta in re.findall(r'\d{11}|[+]\d{11}', meta):
                return True
        # Выше условие, в которое мы проваливаемся при проверке номера,
        # не затрагивая на данном этапе пока еще отсутствующий self.mail_user.
        # Он будет проверяться при вхождении в следующее условие, когда мы введем почту и
        # сохраним в переменную self.mail_user.
        elif data == 'inp_mail':
            domains = ['@mail.ru', '@gmail.com', '@rambler.ru', '@yahoo.com', '@yandex.ru']
            try:
                domain_user = re.findall(r'@+\S+', meta)[0]
            except IndexError:
                return False
            else:
                if domain_user in domains:
                    return True

    # Выше проверка домена почты на соответствие паттерну регулярного выражения и наличие в списке основных
    # существующих доменов. Теперь, когда она существует, мы можем это сделать. Также данный метод будет использоваться
    # при проверке значений, которые вводятся в update(при обновлении базы данных)

    # -------------------------------------------
    @staticmethod
    def found_contacts(fetchall: list) -> list:
        """
        Стат. метод превращения fetchall (списка кортежей найденных строк) в список с подсписками и превращение всех
        элементов подсписков в строки для отображения в БД
        """
        result = list(map(list, fetchall))  # избавляемся от кортежей
        result = list(map(lambda item: list(map(str, item)), result))  # превращаем элементы подсписков в строки
        return result

    # -------------------------------------------
    @staticmethod
    def ignore_RunTimeError(widget: QWidget) -> None:
        """
        Стат. метод игнорирования ошибки RunTimeError. У нас она возникает, когда мы хотим удалить виджет, к которому
        ранее уже был применен метод del_widget().
        """
        try:
            widget.del_widget()
        except RuntimeError:
            pass

    # -------------------------------------------
    # -----Вспомогательные методы для работы с интерфейсом (пояснения по каждому методу написаны рядом с ними)
    def clear_page(self) -> None:
        """
        Метод очистки страницы от виджетов
        """
        for widget in self.widgets_collection:
            self.ignore_RunTimeError(widget=widget)
        # выше применяем метод .ignore_RunTimeError ко всем виджетам в коллекции виджетов для чистого удаления
        self.widgets_collection.clear()  # проводим контрольную очистку списка (на случай оставления ссылок в нем)

    def home_page(self) -> None:
        """
        Метод возврата на начальную страницу
        """
        self.clear_temporary(True)  # очищаем временные списки
        self.clear_page()  # очищаем текущую страницу (на которой был вызван данный метод через кнопку)
        self.page_commands()  # применяем конструктор первой страницы

    def messagebox_method(self, content: str, content_button: str, level_message: str) -> QMessageBox:
        """
        Метод создания всплывающего окна уведомлений
        """
        msg = MessageBox(content, content_button, level_message)
        self.widgets_collection.append(msg)
        return msg

    def label_method(self, right: int, down: int, content: str) -> QLabel:
        """
        Метод для размещения надписи
        """
        label = Label(window, right, down, content)
        self.widgets_collection.append(label)
        return label

    def button_method(self, content: str, right: int, down: int, size: int, func: Callable) -> QPushButton:
        """
        Метод для создания кнопки с функцией внутри при клике
        """
        button = Button(window, content, right, down, size)
        button.click(func)
        self.widgets_collection.append(button)
        return button

    def table_method(self, data: list) -> QTableWidget:
        """
        Метод для создания таблицы
        """
        table = Table(window, data)
        self.widgets_collection.append(table)
        return table

    def checkbox_method(self, right: int, down: int, content: str) -> QCheckBox:
        """
        Метод для создания кнопки вкл/выкл
        """
        checkbox_ex = CheckBox(window=window, content=content, right=right, down=down)
        self.widgets_collection.append(checkbox_ex)
        return checkbox_ex

    def search_data_method(self, content: str, column: str) -> None:
        """
        Метод для поиска контакта по 1 из 3 значений(имя, номер, почта)
        """
        self.clear_page()
        self.label_method(right=200, down=50, content=content)
        self.line = Line(window, right=200, down=70, size=200)
        self.line.line.show()
        self.widgets_collection.append(self.line)

        def search() -> None:
            """
            Сама функция поиска
            """
            line = self.line.line.text()
            if column == 'name':
                db_cont.cursor.execute('''SELECT * FROM Contacts_list WHERE name = :name;''',
                                       {'name': line})
            elif column == 'number':
                db_cont.cursor.execute('''SELECT * FROM Contacts_list WHERE number_phone = :number;''',
                                       {'number': line})
            elif column == 'email':
                db_cont.cursor.execute('''SELECT * FROM Contacts_list WHERE email = :mail;''',
                                       {'mail': line})
            result_data = self.found_contacts(db_cont.cursor.fetchall())
            self.table_method(result_data)
            self.back_button()

        self.button_method(content='Найти контакт', right=150, down=400, size=300, func=search)
        self.back_button()

    def back_button(self) -> None:
        """
        Метод возврата на стартовую страницу с командами
        """
        self.button_method(content=f'Назад к списку команд', right=150, down=450, size=300, func=self.home_page)

    def view_table(self, id_field: bool) -> None:
        """
        Метод отображения всей таблицы (БД)
        """
        db_cont.cursor.execute('''SELECT * FROM Contacts_list;''')

        result_data = self.found_contacts(db_cont.cursor.fetchall())

        self.table_method(result_data)
        if id_field:  # если нам нужно поле для ввода id (чтобы с его помощью управлять строкой)
            self.label_method(right=490, down=50, content=f'Введите id')
            self.id_line = Line(window, right=510, down=70, size=40)
            self.id_line.line.show()
            self.widgets_collection.append(self.id_line)

    # Методы отображения страниц, которые привязаны к определенной команде со стартовой страницы
    # --------------------------
    def page_commands(self) -> None:
        """
        Метод отображения стартовой страницы с командами
        """
        self.clear_page()
        self.label_method(right=240, down=50, content='Выберите команду')
        button_right, button_down, number_button = 150, 75, 1
        for k, v in commands.items():
            self.button_method(content=f'{k}. {v}',
                               right=button_right,
                               down=button_down,
                               size=300,
                               func=self.database_methods[k])
            button_down += 25
            number_button = number_button + 1 if number_button < 10 else 0

    # --------------------------
    def page_insert(self) -> None:
        """
        Метод добавления данных в таблицу (БД)
        """
        self.clear_page()

        self.label_method(right=200, down=30, content='Добавить нового пользователя')

        self.label_method(right=200, down=50, content='Введите имя')  # создание виджета текста
        self.name_line = Line(window, right=200, down=70, size=200)
        self.name_line.line.show()
        self.widgets_collection.append(self.name_line)

        self.label_method(right=200, down=115, content='Введите номер')  # создание виджета текста
        self.number_line = Line(window, right=200, down=135, size=200)
        self.number_line.line.show()
        self.widgets_collection.append(self.number_line)

        self.label_method(right=200, down=180, content='Введите почту')  # создание виджета текста
        self.mail_line = Line(window, right=200, down=200, size=200)
        self.mail_line.line.show()
        self.widgets_collection.append(self.mail_line)

        # --------------------------------
        def insert_database() -> None:
            """
            Метод вставки данные в таблицу (БД)
            """
            name_user = self.name_line.line.text()
            number_user = self.number_line.line.text()
            mail_user = self.mail_line.line.text()
            dates = [name_user, number_user, mail_user]
            if all(dates):
                # all для условия, что все поля НЕ ПУСТЫЕ (#NOT NULL пустую строку НЕ видит как NULL,
                # поэтому тут эта настройка не работает)
                if all([self.patterns(data='inp_num', meta=number_user),
                        self.patterns(data='inp_mail', meta=mail_user)]):
                    try:
                        db_cont.cursor.execute('''INSERT INTO Contacts_list (name, number_phone, email)
                                                VALUES(?,?,?);''', (name_user, number_user, mail_user))
                        db_cont.connection.commit()
                        self.messagebox_method(content=f'Контакт добавлен!', content_button='Закрыть',
                                               level_message='Info')
                    except sqlite3.IntegrityError:
                        self.messagebox_method(content=f'Контакт c такими данными уже есть!',
                                               content_button='Закрыть',
                                               level_message='Warning')
                else:
                    self.messagebox_method(content=f'Телефон и/или почта введены неправильно!',
                                           content_button='Закрыть',
                                           level_message='Warning')

            else:
                dates_booleans = [bool(i) for i in dates]
                warning_messages = {
                    0: lambda: self.messagebox_method(content=f'Поле имени пустое!',
                                                      content_button='Закрыть',
                                                      level_message='Warning'),
                    1: lambda: self.messagebox_method(content=f'Поле номера пустое!',
                                                      content_button='Закрыть',
                                                      level_message='Warning'),
                    2: lambda: self.messagebox_method(content=f'Поле почты пустое!',
                                                      content_button='Закрыть',
                                                      level_message='Warning')
                }
                [warning_messages.get(data[0])() for data in enumerate(dates_booleans) if not data[1]]

        self.button_method(content=f'Занести данные в базу', right=150, down=400, size=300, func=insert_database)
        self.back_button()

    # --------------------------
    def page_search_name(self) -> None:
        """
        Метод нахождения контакта по имени
        """
        self.search_data_method(content=f'Поиск контакта по имени (введите имя)', column='name')

    def page_search_number_mail(self) -> None:
        """
        Метод нахождения контакта по почте или телефону
        """
        self.clear_page()
        self.label_method(right=150, down=50, content=f'По каким данным вы хотите найти контакт?')

        def search_number() -> None:
            """
            Метод нахождения контакта по номеру
            """
            self.search_data_method(content='Введите номер телефона', column='number')

        def search_mail() -> None:
            """
            Метод нахождения контакта по электронной почте
            """
            self.search_data_method(content='Введите электронную почту', column='email')

        self.button_method(content='Найти по номеру телефона', right=150, down=125, size=300, func=search_number)
        self.button_method(content='Найти по электронной почте', right=150, down=150, size=300, func=search_mail)

        self.back_button()

    # --------------------------

    def page_update(self) -> None:
        """
        Страница метода обновления данных контакта
        В ней первой строкой мы очищаем временный список. Даже если он еще не создан, программа не падает благодаря
        магическому методу __gettatr__. Не созданный объект возвращает то, что возвращает этот метод, т.е. 0
        """
        self.clear_temporary(True)  # очищаем временный список
        self.clear_page()  # очищаем страницу

        def page_update_local():
            """
            Следующая страница метода
            """

            def query_update(*args):
                """
                Функция внесения изменений в БД
                """
                name, number, email = args  # Данные для БД
                db_cont.cursor.execute('''UPDATE Contacts_list SET name=:name, number_phone=:number,email=:email
                                        WHERE id=:id;''', dict(name=name, number=number, email=email, id=self.id_text))
                db_cont.connection.commit()  # меняем данные и коммитим результат
                self.messagebox_method(content=f'Данные обновлены!',
                                       content_button='Закрыть',
                                       level_message='Info')  # всплывающее сообщение

            self.id_text = self.id_line.line.text()  # id контакта. self.id_line находится в методе self.view_table
            db_cont.cursor.execute('''SELECT * FROM Contacts_list WHERE id=:id;''',
                                   {'id': self.id_text})  # Выбор контакта по его id
            self.result_data = self.found_contacts(db_cont.cursor.fetchall())  # Преобразование данных контакта
            if not len(self.result_data):  # если контакт по id не найден
                self.messagebox_method(content='Контакта с таким id не найдено!',
                                       content_button='Закрыть',
                                       level_message='Warning')  # всплывающее сообщение
            else:  # если контакт найден
                self.clear_page()  # очищаем страницу
                self.table_method(self.result_data)  # показ выбранного контакта в табличном виде
                self.label_method(right=160, down=100, content='Вы хотите изменить одно значение или все?')  # надпись

                def one_value():
                    """
                    Функция изменения ОДНОГО значения
                    """
                    self.clear_temporary()  # безопасная очистка временного списка self.temporary

                    label = self.label_method(right=225, down=150, content='Какое хотите изменить?')  # надпись
                    self.temporary.append(label)  # добавляем надпись во временный список

                    def line_for_change(data_change):
                        """
                        Функция с полем для ввода новых данных
                        """
                        self.clear_temporary()  # очищаем и пересоздаем self.temporary

                        self.label = self.label_method(right=200,
                                                       down=200,
                                                       content=f'Введите новые данные: {data_change}')  # надпись
                        self.temporary.append(self.label)  # добавляем надпись во временный список

                        self.line_data = Line(window, right=200, down=220, size=200)  # поле для ввода данных
                        self.line_data.line.show()  # размещение поля для ввода данных

                        # self.widgets_collection.append(self.line_data)  # добавление виджета поля к общим виджетам
                        self.temporary.append(self.line_data)  # добавление виджета поля во временный список

                        def change_data():
                            """
                            Функция, вызывающая query_update, если все ок
                            """
                            new_data, contacts = self.line_data.line.text(), self.result_data[0][1:]
                            if data_change == 'Имя':  # если хотим изменить Имя контакта
                                contacts[0] = new_data  # меняем его по индексу в списке данных контакта
                                query_update(*contacts)  # закидываем распакованный список во вспомогательную функцию
                            else:
                                data_for_pattern = {'Номер': 'inp_num', 'Почта': 'inp_mail'}  # словарь данных
                                if self.patterns(data=data_for_pattern[data_change], meta=entered_text):
                                    if data_change == 'Номер':  # если номер соответствует паттерну, то меняем его
                                        contacts[1] = new_data
                                        query_update(*contacts)
                                    elif data_change == 'Почта':  # если почта соответствует паттерну, то меняем её
                                        contact[2] = new_data
                                        query_update(*contacts)
                                else:
                                    self.messagebox_method(content=f'{data_change} не соответствует формату!',
                                                           content_button='Закрыть',
                                                           level_message='Warning')  # всплывающее сообщение

                        change_button = self.button_method(content='Внести изменения',
                                                           right=225,
                                                           down=260,
                                                           size=150,
                                                           func=change_data)  # кнопка запуска функции change_data
                        self.temporary.append(change_button)  # добавление во временный список кнопки
                        self.back = self.button_method(content='Назад', right=245, down=375, size=100, func=one_value)
                        self.temporary.append(self.back)  # Размещение кнопки "назад" и добавление ее во врем. список

                    functions_button = {
                        0: lambda: line_for_change(data_change='Имя'),
                        1: lambda: line_for_change(data_change='Номер'),
                        2: lambda: line_for_change(data_change='Почта')
                    }  # словарь функций для кнопок

                    down = 170
                    for column in enumerate(['Имя', 'Номер телефона', 'Почта']):
                        btn = self.button_method(content=column[1],  # кнопка обращения к функциям в словаре выше
                                                 right=225,
                                                 down=down,
                                                 size=150,
                                                 func=functions_button[column[0]])
                        down += 25
                        self.temporary.append(btn)

                def all_value():
                    """
                    Функция изменения ВСЕХ значений в строке контакта
                    """
                    self.clear_temporary()  # вызов метода очищения временного списка с виджетами
                    down_label = 160  # координата низа верхней (первой) надписи
                    self.lines = []  # временный список для полей типа QLineWidget
                    for field in ['Имя', 'Номер телефона', 'Почта']:  # цикл по именам колонн таблицы
                        label = self.label_method(right=230, down=down_label, content=field)  # надпись
                        self.temporary.append(label)  # добавление надписи во временный список
                        line_data = Line(window, right=230, down=down_label + 20, size=130)  # поле ввода
                        line_data.line.show()  # размещение поля ввода
                        self.lines.append(line_data)  # добавление поля ввода во временный список для полей
                        self.temporary.append(line_data)
                        down_label += 50

                    def change_data():
                        """
                        Функция, вызывающая query_update, если все о
                        """
                        text_number = self.lines[1].line.text()  # введенный текст нового номера.
                        text_mail = self.lines[2].line.text()  # введенный текст новой почты
                        patterns_ok = [self.patterns(data='inp_num', meta=text_number),
                                       self.patterns(data='inp_mail', meta=text_mail)]
                        if not all(patterns_ok):  # если номер или почта не соответствуют паттерну
                            self.messagebox_method(content='Номер и/или почта не соответствуют формату!',
                                                   content_button='Закрыть',
                                                   level_message='Warning')
                        else:  # есл все ок, то заносим в базу данных через query_update
                            query_update(*[widget_line.line.text() for widget_line in self.lines])

                    change_button = self.button_method(content='Внести изменения',
                                                       right=225,
                                                       down=350,
                                                       size=150,
                                                       func=change_data)
                    self.temporary.append(change_button)

                def some_value():
                    """
                    Функция изменения НЕСКОЛЬКИХ значений
                    """
                    self.clear_temporary()  # вызов метода очищения временного списка с виджетами
                    label = self.label_method(right=215, down=150, content='Выберите, что хотите поменять')
                    self.temporary.append(label)
                    checkbox_down = 180
                    for column in ['Имя', 'Номер', 'Почта']:  # размещение трех кнопок выбора, какое значение будем изм.
                        check = self.checkbox_method(right=280, down=checkbox_down, content=column)
                        checkbox_down += 25
                        self.temporary.append(check)

                    def data_selection():
                        """
                        В этой функции размещаются поля ввода для включенных кнопок
                        """
                        down = 200
                        for widget in self.temporary:
                            if hasattr(widget, 'checkbox') and widget.checkbox.checkState():
                                text_on_line = widget.checkbox.text()
                                self.label = self.label_method(right=250, down=down - 20, content=text_on_line)
                                line_data = Line(window, right=250, down=down, size=130)

                                line_data.line.show()
                                self.lines.append([self.label, line_data])
                                down += 50

                        if not self.lines:  # если нет полей (т.е. если кнопки не нажаты)
                            self.messagebox_method(content='Выберите данные, которые хотите изменить!',
                                                   content_button='Закрыть', level_message='Warning')
                        else:  # если хотя бы одно поле существует (хотя бы одна кнопка нажата)
                            self.clear_temporary()
                            self.temporary = self.lines
                            self.change = self.button_method(content='Внести изменения', right=205, down=down - 20,
                                                             size=200, func=change_data)
                            self.back = self.button_method(content='Назад', right=250, down=380, size=100,
                                                           func=some_value)

                            self.temporary.append(self.change)
                            self.temporary.append(self.back)

                    def change_data():
                        """
                        Функция, вызывающая query_update, если все ок
                        """
                        text_lines_bool = all([i[1].line.text() for i in self.temporary if isinstance(i, list)])
                        if not text_lines_bool:  # если не все выбранные поля заполнены
                            self.messagebox_method(content='Не все поля заполнены!',
                                                   content_button='Закрыть',
                                                   level_message='Warning')
                        else:  # если все ок
                            text_data, contact = [], self.result_data[0][1:]

                            def mutate_contact(db_column: int, data: str):
                                """
                                Функция изменение данных в столбце
                                """
                                contact[db_column] = data

                            mutate_functions = {
                                'Имя': lambda data: mutate_contact(db_column=0, data=data),
                                'Номер': lambda data: mutate_contact(db_column=1, data=data),
                                'Почта': lambda data: mutate_contact(db_column=2, data=data)
                            }  # словарь с вызовами функций изменения через лямбду, к которому мы обращаемся ниже

                            for element in self.temporary:  # цикл по временному списку
                                if isinstance(element, list):  # если мы попали на подсписок (в подсписках поля ввода)
                                    column_name = element[0].text.text()  # имя столбца
                                    new_data = element[1].line.text()  # текст из поля ввода
                                    mutate_functions[column_name](new_data)  # преобразуем список contact

                            patterns_ok = [self.patterns(data='inp_num', meta=contact[1]),
                                           self.patterns(data='inp_mail', meta=contact[2])]  # проверяем паттерны
                            if not all(patterns_ok):  # если не соответствует паттерну - выводим сообщение
                                self.messagebox_method(content='Номер и/или почта не соответствуют формату!',
                                                       content_button='Закрыть',
                                                       level_message='Warning')
                            else:  # если все ок - добавляем в базу данные
                                query_update(*contact)

                    enter = self.button_method(content='Далее', right=225, down=350, size=150, func=data_selection)
                    self.temporary.append(enter)  # кнопка запуска функции data_selection

                self.button_one = self.button_method(content='Одно', right=160, down=120, size=100, func=one_value)
                self.button_all = self.button_method(content='Все', right=350, down=120, size=100, func=all_value)
                self.button_some = self.button_method(content='Несколько', right=255, down=120, size=100,
                                                      func=some_value)
                self.button_method(content='Назад к таблице', right=225, down=410, size=150, func=self.page_update)
                self.back_button()  # кнопки передвижения по страницам

        self.view_table(id_field=True)  # показ таблицы БД с полем ввода ID

        self.button_method(content='Ок', right=470, down=70, size=40, func=page_update_local)  # кнопка "Ок"
        self.button_method(content='Назад', right=470, down=450, size=100, func=self.home_page)  # кнопка "Назад"

    # --------------------------
    def del_page(self):
        """
        Метод удаления страницы
        """
        self.clear_page()  # очищаем страницу
        self.view_table(id_field=True)  # показываем таблицу с полем ввода

        def del_contact():
            """
            Функция удаления контакта
            """
            del_id = field_del.line.text()  # введенный id сохраняем в переменную
            db_cont.cursor.execute('''SELECT * FROM Contacts_list;''')  # выбор всей БЖ
            all_contacts_id = [contact[0] for contact in self.found_contacts(db_cont.cursor.fetchall())]  # все id из БД
            if del_id in all_contacts_id:  # если введенный id есть в списке всех id
                db_cont.cursor.execute('''DELETE FROM Contacts_list WHERE id=:id;''', {'id': del_id})
                db_cont.connection.commit()  # удаляем контакт по этом id и коммитим
                self.messagebox_method(content='Контакт удален', content_button='Закрыть', level_message='Warning')
            else:  # если id нет в списке всех id
                self.messagebox_method(content='Контакт с таким id отсутствует!',
                                       content_button='Закрыть',
                                       level_message='Warning')  # выводим соответствующие сообщения

        self.button_method(content='Удалить', right=480, down=100, size=100, func=del_contact)  # кнопка удаления
        self.button_method(content='Назад', right=470, down=450, size=100, func=self.home_page)  # кнопка возврата

    # --------------------------
    def record_yaml_page(self):
        """
        Метод записи базы данных в файл YAML-формата
        """
        db_cont.cursor.execute('''SELECT * FROM Contacts_list;''')  # Выбираем всю БД
        tuple_users = db_cont.cursor.fetchall()  # Выбираем все данные из БД в кортеж.
        dict_contacts = {'База контактов':
                             {f'Контакт {i[0]}':
                                  [f'Имя: {i[1]}', f'Номер: {i[2]}', f'Почта: {i[3]}'] for i in tuple_users
                              }
                         }  # словарь для загрузки в YAML файл
        with open('contacts_file_PYQT5.yaml', 'w', encoding='UTF-8') as yaml_PyQT5:
            yaml.dump(dict_contacts, yaml_PyQT5, allow_unicode=True)  # загрузка в YAML файл
        self.messagebox_method(content='Файл успешно создан/перезаписан',
                               content_button='Закрыть',
                               level_message='Info')  # Сообщение о загрузке

    # --------------------------
    def load_from_yaml(self) -> None:
        """
        Метод выгрузки данных из файла YAML
        """
        self.clear_page()
        with open('contacts_file_PYQT5.yaml') as file_for_load:
            data_dict = yaml.load(file_for_load, Loader=FullLoader)  # выгрузка из файла yaml в словарь

        values_data = list(data_dict.values())  # первичные значения словаря

        keys_data = list(values_data[0].keys())  # Ключи из списка выше. Содержит слово "контакт" и его id.

        primary_keys = [pk[1] for pk in [key.split() for key in keys_data]]  # извлечение id из ключей выше

        dates_users = list(values_data[0].values())  # извлечение данных контактов

        [dates_users[primary_keys.index(i)].insert(0, i) for i in primary_keys]  # слияние данных контактов с их id

        id_dates = []
        for i in dates_users:  # избавление строк от наименований столбцов
            id_dates.append(list(map(lambda el: re.findall(r' (\S+)', el)[0] if not el.isdigit() else el, i)))

        self.table_method(id_dates)  # вывод в таблицу
        self.button_method(content='Назад', right=470, down=450, size=100, func=self.home_page)  # кнопка возврата

    # --------------------------
    def clear_table(self) -> None:
        """
        Метод для полной очистки таблицы
        """
        self.clear_page()  # очищаем страницу
        self.view_table(id_field=False)  # показ таблицы без поля ввода первичного ключа
        self.label_method(right=500, down=50, content='Очистить\nтаблицу?')  # надпись с вопросом

        def clear():
            """
            Функция очистки
            """
            message = self.messagebox_method(content='Таблица будет полностью очищена!\nВы уверены?',
                                             content_button=None,
                                             level_message='Question')  # всплывающее окно
            if message.msg.clickedButton().text() == 'Да':  # если текст в нажатой кнопке == 'Да'
                db_cont.cursor.execute('''DELETE FROM Contacts_list WHERE id > 0;''')  # чистим БД
                db_cont.connection.commit()  # коммитим и обнуляем счетчик pk
                db_cont.cursor.execute('''UPDATE sqlite_sequence set seq = 0 where name = 'Contacts_list';''')
            else:  # ничего не делаем, только закрываем всплывающее окно
                pass

        self.button_method(content='Да', right=500, down=100, size=50, func=clear)  # кнопка запуска функции clear
        self.button_method(content='Назад', right=470, down=450, size=100,
                           func=self.home_page)  # кнопка возврата в меню

    # --------------------------
    def random_values(self) -> None:
        """
        Метод генерации случайных данных
        """
        self.clear_page()  # очищаем страницу
        faker_ = Faker('ru-RU')  # экземпляр класса Faker с настройками для данных на латинице
        space = ' '  # пробел для конкатенации
        self.label_method(right=200, down=100, content=f'Сколько случайных пользователей\n{space * 16}нужно создать?')
        quantity = Line(window, right=285, down=140, size=50)  # поле для ввода количества случайных контактов
        quantity.line.show()  # размещение поля
        self.widgets_collection.append(quantity)  # добавляем в главную коллекцию виджетов

        def insert_random() -> None:
            """
            Функция генерации данных
            """
            quantity_contacts = int(quantity.line.text())  # введенная цифра числа контактов, которые нужно создать
            try:
                for i in range(quantity_contacts):  # на каждой итерации цикла генерируется один контакт
                    name_contact = faker_.first_name_male()  # случайное имя
                    number_contact = int(f'89{random.randint(100000000, 999999999)}')  # случайный номер
                    mail_contact = faker_.ascii_free_email()  # случайная почта
                    db_cont.cursor.execute('''INSERT INTO Contacts_list(name, number_phone, email)
                                                    VALUES(?, ?, ?);''',
                                           [name_contact, number_contact, mail_contact])  # генерируем
            except ValueError:  # если в поле для ввода числа мы ввели не число
                self.messagebox_method('Поле пустое или заполнено НЕ цифрами!',
                                       'Закрыть', 'Info')
            else:
                db_cont.connection.commit()  # если все ок - коммитим БД и выводим соответствующее сообщение

                self.messagebox_method('Данные сгенерированы', 'Закрыть', 'Info')

        self.button_method(content='Добавить контакты', right=210, down=180, size=200, func=insert_random)
        self.back_button()  # кнопка возврата и генерации контактов

    # --------------------------
    def view_page(self) -> None:
        """
        Метод показа страницы со всей базой данных в табличном виде
        """
        self.clear_page()  # очищаем страницу
        self.view_table(id_field=False)  # показываем таблицу
        self.button_method(content='Назад', right=470, down=450, size=100, func=self.home_page)  # кнопка возврата

    # --------------------------
    def __getattr__(self, item: list) -> int:
        """
        Маг. метод для обхода ошибки при несуществующих атрибутах класса
        """
        return 0

    # --------------------------
    def clear_temporary(self, *all_lists: bool) -> list:
        """
        Метод очистки временных списков
        """

        def exam_widget(wid: QWidget) -> None:
            """
            Функция индивидуального удаления виджета или списка виджетов
            """
            wid.del_widget() if not isinstance(wid, list) else [element.del_widget() for element in wid]

        if self.temporary and len(self.temporary) > 0:
            [exam_widget(wid=widget) for widget in self.temporary]
            self.temporary = []
        else:
            self.temporary = []
        if all_lists:
            if self.lines and len(self.lines) > 0:
                [exam_widget(widget) for widget in self.lines]
                self.lines = []
            else:
                self.lines = []


# --------------------------
def main() -> None:
    """
    Головная функция запуска
    """
    App()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
