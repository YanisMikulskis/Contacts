# Конечно! Вот сложное задание на Python для вас:
# Задание: Внедрение системы управления контактами
# Создайте систему управления контактами на основе командной строки с помощью Python. Система должна позволять
# пользователям выполнять следующие операции:
# Добавить контакт: Пользователи должны иметь возможность добавить новый контакт с такими данными, как имя, номер
# телефона и адрес электронной почты.
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
import random
import sqlite3
import time
import sys
import yaml
from yaml.loader import FullLoader
import re
from faker import Faker


def patterns(data: str, meta: str) -> bool:  # ф-ция для проверки введенных (или измененных) значений для тел. и почты

    if data == 'input_number':
        if meta in re.findall(r'\d{11}|[+]\d{11}', meta):
            return True
    # Выше условие, в которое мы проваливаемся при проверке номера,
    # не затрагивая на данном этапе пока еще несуществующий self.mail_user.
    # Он будет проверяться при вхождении в следующее условие, когда мы введем почту и
    # сохраним в переменную self.mail_user.
    elif data == 'input_mail':
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


class DATABASE:
    def __init__(self, name_database: str):
        self.new_name: str = None
        self.new_number: int = None
        self.new_email: str = None
        self.name_database: str = name_database
        self.connection = sqlite3.connect(self.name_database)
        self.cursor = self.connection.cursor()

    # -----------------------
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
    def ins_table(self):  # добавить данные в таблицу
        name_user = input('введите имя ')
        number_user = input('введите номер ')
        # проверим соответствие правильному вводу через метод patterns()
        if not patterns('input_number', number_user):
            print(f'Номер введен неверно! Попробуйте еще раз')
            return
        mail_user = input('введите почту ')

        if not patterns('input_mail', mail_user):
            print(f'Почта введена неверно! Попробуйте еще раз')
            return
        try:
            self.cursor.execute('''INSERT INTO Contacts_list (name, number_phone, email) 
                                    VALUES(?,?,?);''', (name_user, number_user, mail_user))

        except sqlite3.IntegrityError:
            print(f'Контакт с такими данными уже есть!')
        self.connection.commit()

    # -----------------------
    def ins_table_random_data(self):  # заполнение БД случайными данными с помощью библиотеки Faker и Random
        faker_ = Faker('ru-RU')
        quantity = int(input(f'Сколько случайных пользователей вы хотите создать?'))
        for i in range(quantity):
            name_user = faker_.first_name_male()
            number_user = int(f'89{random.randint(111111111, 999999999)}')
            mail_user = faker_.ascii_free_email()
            self.cursor.execute('''INSERT INTO Contacts_list (name, number_phone, email)
                                    VALUES(?, ?, ?)''', (name_user, number_user, mail_user))
            self.connection.commit()
        print(f'--------\nДанные сгенерированы!\n--------')
        time.sleep(1)

    # -----------------------
    def search_name(self, arg_name: str) -> str:  # поиск контакта по имени
        self.cursor.execute('''SELECT * FROM Contacts_list WHERE name = :name;''', {'name': arg_name})
        # выше выбираем подходящие контакты, имя которых совпадает с параметром метода
        dict_data = dict()

        # Ниже рекурсивное извлечение данных из fetchall. Это список кортежей. Каждый кортеж - одна строка таблицы.
        # А нужные строки мы выбираем выше через SELECT. Через рекурсию заносим данные в словарь(выше) для
        # более удобного чтения.
        def info(sql_data: tuple, idx: int, key: int):
            if idx == len(sql_data):
                return
            dict_data.setdefault(key, list(sql_data[idx][1:]))
            idx += 1
            key += 1
            return info(sql_data, idx, key)

        info(self.cursor.fetchall(), 0, 1)
        print(f'----------')
        print(f'Найденные результаты\n') if dict_data else print(f'Контакт не найден!')
        for k, v in dict_data.items():  # Цикл по словарю для более удобного отображения данных в нем
            print(f'Пользователь {k}\nИМЯ: {v[0]}\nНОМЕР ДЛЯ СВЯЗИ: {v[1]}\nЭЛ.ПОЧТА: {v[2]}\n')
        print(f'----------')

    # -----------------------
    def search_number_mail(self, arg_meta: str) -> str:  # поиск контакта по почте или номеру
        if arg_meta == '1':
            input_mail = input(f'Введите почту для поиска: ')
            self.cursor.execute('''SELECT * FROM Contacts_list 
                                        WHERE email = :input_mail;''',
                                {'input_mail': input_mail})

        elif arg_meta == '2':
            input_number = int(input(f'Введите номер для поиска: '))
            self.cursor.execute('''SELECT * FROM Contacts_list 
                                        WHERE number_phone = :input_number;''',
                                {'input_number': input_number})

        if self.cursor.fetchall():  # если контакт найден
            for i in self.cursor.fetchall():
                print(f'ИМЯ: {i[1]}\nНОМЕР ДЛЯ СВЯЗИ: {i[2]}\nЭЛ.ПОЧТА: {i[3]}')
        else:
            print(f'Контакт с такими данными не найден!')
            time.sleep(1)

    # -----------------------
    def update(self):  # изменение контакта
        print(f'Какой именно контакт вы хотите изменить? Введите его id')

        for user in self.cursor.fetchall():
            print(f'id:{user[0]}, имя: {user[1]}, номер: {user[2]}, мыло: {user[3]}')

        id_user = input(f'id контакта: ')
        self.cursor.execute('SELECT * FROM Contacts_list WHERE id=:id_user', {'id_user': id_user})

        execute_user = self.cursor.fetchall()[0][
                       1:]  # fetchall срабатывает только один раз! потом нужно опять работать с SELECT

        change = int(input(f'Вы хотите изменить одно значение или все?\nНажмите 1, если одно. Иначе - 2\nВВОД: '))
        if change == 1:  # если пользователь захочет изменить ОДНО значение
            var_change = int(input('Выберите значение, которое хотите изменить\n1 - Имя, 2 - Номер, 3 - почта'))
            values = {
                # используются анонимные функции, так как без них прочитывается весь словарь и просит
                # вводить все значения
                1: lambda: input('Новое имя!: '),
                2: lambda: int(input('Новый номер!: ')),
                3: lambda: input('Новая почта!: ')
            }

            # НИЖЕ сохранение нового ОДНОГО значения в переменную. Нужно ее также проверить через регулярные выражения,
            # как проверялись данные при вводе(соответствие почты и телефона паттерну соответствующих регулярных
            # выражений)

            new_value = values[var_change]()
            if var_change == 2 and not patterns('number', str(new_value)):
                print(f'Новый номер введен неверно!')
                return
            elif var_change == 3 and not patterns('mail', new_value):
                print(f'Новая почта введена неверно!')
                return
            # ниже присваем соответствующему значению новые данные, а остальные оставляем ьез изменений
            self.new_name = new_value if var_change == 1 else execute_user[0]
            self.new_number = new_value if var_change == 2 else execute_user[1]
            self.new_email = new_value if var_change == 3 else execute_user[2]

        elif change == 2:  # если пользователь выбрал изменить все значения
            self.new_name = input('Новое имя: ')
            self.new_number = int(input('Новый номер: '))
            self.new_email = input('Новая почта: ')

        self.cursor.execute(''' UPDATE Contacts_list 
                                SET name=:name,
                                    number_phone=:number_phone,
                                    email=:email 
                                    WHERE id=:id; ''',
                            dict(name=self.new_name, number_phone=self.new_number, email=self.new_email, id=id_user))
        print(f'\nИзменено!\n')
        self.connection.commit()

    # -----------------------
    def del_contact(self, id_user_del: int) -> str:  # удалить контакт
        self.cursor.execute('''DELETE FROM Contacts_list WHERE id=:id;''', {'id': id_user_del})
        self.connection.commit()  # коммитим БД и сбрасываем id до максимального существующего значения
        self.cursor.execute('''UPDATE sqlite_sequence set seq = 0 where name = 'Contacts_list';''')
        # выше сброс id до максимального существующего значения
        print(f'Контакт удален!\nнажмите Enter, чтобы продолжить')

    # -----------------------
    def record_in_yaml(self):  # загрузка в файл формата yaml
        self.cursor.execute('''SELECT * FROM Contacts_list;''')
        tuple_users = self.cursor.fetchall()
        dict_users = {
        }
        for user in tuple_users:  # создаем словарь, чтобы потом удобнее можно было загрузить в yaml
            key = f'Пользователь {user[0]}'
            val = [
                f'Имя: {user[1]}',
                f'Номер: {user[2]}',
                f'Почта: {user[3]}'
            ]
            dict_users.setdefault(key, val)
        dict_database = {f'База контактов': dict_users}
        print(dict_database)
        with open('contacts_file.yaml', 'w', encoding='utf-8') as file_yaml:
            yaml.dump(dict_database, file_yaml, allow_unicode=True)  # загрузка в файл yaml

    # -----------------------
    def load_from_yaml(self):  # выгрузка данных из файла YAML
        with open('contacts_file.yaml') as file_for_load:
            data_dict = yaml.load(file_for_load, Loader=FullLoader)  # FullLoader - для выгрузки без ограничений
        data_list = []

        def extraction(di_values, idx):  # рекурсивное извлечение нужных данных словаря из YAML-файла
            if idx > len(di_values) - 1:
                return
            if isinstance(di_values[idx], dict):
                extraction(list(di_values[idx].values()), 0)
            else:
                data_list.append(di_values[idx])
            idx += 1
            return extraction(di_values, idx)

        extraction(list(data_dict.values()), 0)
        # ниже избавление от лишних слов в данных каждого пользователя
        # например: было #[['Имя: Виктор', 'Номер: 79999999999', 'Почта: mail@mail.ru']]
        # при обработке данного примера выражением ниже получится [['Виктор', '79999999999', 'mail@mail.ru']]
        # Данные записи будут загружаться в базу данных, поэтому мы избавились от лишних слов
        data_list = [list(map(lambda x: re.findall(r':\s+([^\n]+)', x)[0], i)) for i in data_list]
        # ниже преобразование номера в числовое значение, так как изначально все выгружается в формате str
        data_list = [list(map(lambda x: int(x) if x.isdigit() else x, i)) for i in data_list]

        # заносим данные полученного списка в БД
        for item in data_list:
            self.cursor.execute('''INSERT INTO Contacts_list (name, number_phone, email) VALUES(?, ? ,?)''', item)
            self.connection.commit()

    # -----------------------
    def del_table(self):  # Удаление таблицы
        self.cursor.execute('''DROP TABLE Contacts_list;''')

    # -----------------------
    def clear_table(self):  # Очистка таблицы
        self.cursor.execute('''DELETE FROM Contacts_list WHERE id > 0;''')
        self.connection.commit()
        self.cursor.execute(
            '''UPDATE sqlite_sequence set seq = 0 where name = 'Contacts_list';''')  # обнуление автоинкремента id

    # -----------------------
    def view_table(self) -> str:  # Показ таблицы
        self.cursor.execute(''' SELECT * FROM Contacts_list; ''')
        print('-------------------------')
        for contact in self.cursor.fetchall():
            print(f'{contact[0]}: {contact[1]}, {contact[2]}, {contact[3]}')
        print('-------------------------')
        return self.cursor.fetchall()  # return добавляем, чтобы результат возврата данного метода можно было
        # использовать в других методах этого класса


# -----------------------
db_cont = DATABASE(f'contacts')
db_cont.create_table()

database_executes = {
    1: lambda: db_cont.ins_table(),
    2: lambda: db_cont.search_name(input('Введите имя для поиска ')),
    3: lambda: db_cont.search_number_mail(input(f'Искать по почте (1) или по номеру (2)?')),
    4: lambda: db_cont.update(),
    5: lambda: db_cont.del_contact(int(input(f'Введите id контакта, который требуется удалить'))),
    6: lambda: db_cont.record_in_yaml(),
    7: lambda: db_cont.load_from_yaml(),
    8: lambda: db_cont.clear_table(),
    9: lambda: db_cont.ins_table_random_data(),
    10: lambda: db_cont.view_table(),
    0: lambda: exit()  # вызов функции выхода из цикла в анонимной функции лямбда
}

while 1:

    def views():
        print(f'Что хотите сделать?')
        commands = {
            1: 'Добавить контакт',
            2: 'Поиск контакта по имени',
            3: 'Поиск контакта по почте или телефону',
            4: 'Обновить данные контакта',
            5: 'Удалить контакт по его id',
            6: 'Записать в файл формата YAML',
            7: 'Выгрузить из файла формата YAML',
            8: 'Очистить таблицу',
            9: 'Заполнить таблицу случайными данными с помощью библ. Faker',
            10: 'Показать базу данных',
            0: 'Выйти'
        }
        for k, v in commands.items():
            print(f'{v} - нажмите {k}')
        # функции для взаимодействия с БД для сокращения кода

        user_command = int(input('Введите команду: '))

        database_executes[user_command]()


    views()
