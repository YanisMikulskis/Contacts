# Contacts
 A project to implement a database using a graphical interface. The task itself for its implementation was generated in a neural network.

Само задание было получено от нейросети ChatGPT 3.

Задание:
"Внедрение системы управления контактами.

Создайте систему управления контактами на основе командной строки с помощью Python. Система должна позволять
пользователям выполнять следующие операции:

Добавить контакт: Пользователи должны иметь возможность добавить новый контакт с такими данными, как имя,
номер телефона и адрес электронной почты.

Поиск контакта: Пользователи должны иметь возможность искать контакт по имени и получать его данные.

Обновить контакт: Пользователи должны иметь возможность обновить данные существующего контакта.

Удалить контакт: Пользователи должны иметь возможность удалить контакт.

Список всех контактов: Пользователи должны иметь возможность просматривать все контакты, хранящиеся в системе.

Сохранить контакты в файл: Контакты должны быть сохранены в файле, чтобы их можно было восстановить позже даже после
закрытия программы.

Загрузить контакты из файла: При запуске программы она должна загрузить ранее сохраненные контакты из файла.

Обработка ошибок: Внедрите надлежащую обработку ошибок для таких случаев, как недопустимый ввод, контакт не найден
и т. д.

Необязательные задачи:

Внедрить проверку номеров телефонов и адресов электронной почты.

Добавьте функционал искать контакты по номеру телефона или адресу электронной почты.

Создайте простой графический интерфейс с помощью Tkinter или PyQt для лучшего пользовательского интерфейса.
Разрешить пользователям экспортировать контакты в различные форматы, такие как CSV или JSON.

Это задание проверит ваши навыки обработки данных, ввода-вывода файлов, обработки пользовательского ввода и управления
ошибками в Python. Не стесняйтесь расширять или изменять требования в соответствии с вашими предпочтениями. Удачи!"
## Readme
В данном проекте имеется две версии:

1) С графическим интерфейсом от библиотеки PyQT5 (файл by_ChatGTP_and_PyQT5.py). Данный Readme ориентирован именно на 
   нее
2) Без графического интерфейса. Взаимодействие с базой данных осуществляется через командную строку (файл by_ChatGTP.py).
   В общем и целом, тот же принцип работы и логики, только проще, так как нет графических элементов. Можно ссылаться
   на данный Readme для понимания. Одно из существенных отличий программ: в PyQT5 при выгрузке из YAML данные выгружаются
   в таблицу на экране,а в обычном файле выгружается в БД. Эти два механизма реализованы специально, для более
   разнообразного применения языка. Также, в версии с графическим интерфейсом реализована более глубокая функция изменения
   существующих контактов.

К каждому из файлов подключена (или создается при первом запуске) своя соответствующая база данных 
(contacts, contacts_pyqt5). База данных создается с помощью SQlite. Импорты классов виджетов происходят из файла 
Widgets.py. Памятка по установке привязанного к этому проекту виртуального окружения и интерпретатора находится в файле 
virtual_env_and_python.md.

К каждой функции и методу прописаны hints. Если функция (метод) непосредственно сама ничего не возвращает, то
добавляется -> None. Проще говоря, если нет return, относящегося к функции.


## Стек

- Python > 3.11
- PyQT5
- SQlite 3
- PyCharm Professional
- macOS Sonoma ver.14.4.1

## Лицензия

MIT

## Общее описание работы кода (инструкция)

## 1. by_ChatGTP_and_PyQT5.py

1) app = QApplication(sys.argv)
     

    активация приложения для PyQT5

2) class DATABASE_PyQT5: etc.


    В данном классе создается база данных, с которой мы будем работать. Срабатывает единожды при запуске файла. 
    Создается БД 'contacts_pyqt5'.
    Построчные подробности написаны в комменариях в коде рядом со строками.
3) commands

    
    Словарь команд. Все названия команд, который будут у нас в кнопках на главном экране перечислены тут. На ключи этого
    словаря мы будем ссылаться ниже.

4) class App: etc.

    
    Основной класс приложения. Тут будет находиться вся основная логика, все методы и функции для работы с БД.
    Пояснения ко всему см. ниже.

## App

В данном руководстве представлена общая логика работы класса App.

1) __init__()


    Создание основных атрибутов, которые будут использоваться в течении всей работы. Пояснения к каждому см. 
    в комментариях кода
## Вспомогательные методы
2) patterns (staticmethod)

    
    Статичный метод. Данный метод будет использоваться для проверки соответствия вводимых данных.
    Используется в двух методах: при вводе добавлении значений в БД и при их изменении.
    Имеет два параметра: 
    1) data - параметр для определения, какие именно данные будут проверяться. При data = 'inp_num' или data = 'inp_mail'
    проверяется номер и почта соответственно. Номер проверяется на соответствие регулярному выражению. В нем должны быть
    любые 11 цифр ИЛИ "+" в начале любые 11 цифр. В почте мы сначала проверяем домен на соответствие регулярному выражению.
    Если проверка пройдена, проверяем домен на соответсвие одному из вариантов в списке domains. Если все ок, то возвращаем
    True. 
    2) meta - параметр, в которое попадает проверяемое значение.
    Если данный метод возвращает True при проверке почты или номера - проверка пройдена.

3) found_contacts (staticmethod)


    Статичный метод. Данный метод будет использоваться для преобразования результата db_cont.cursor.fetchall() в 
    двумерный массив (список из списков, наполненных строчными данными). db_cont.cursor.fetchall() - команда, 
    которая выполняется выполняется исключительно столько раз, сколько раз мы выполняем команду db_cont.cursor.execute.
    db_cont.cursor.execute - команда, позволяющая взаимодействовать с БД на языке SQL
    db_cont.cursor.fetchall - команды, выводящая в память (при print(db_cont.cursor.fetchall) и на экран) результаты выполнения
    команды db_cont.cursor.execute.
    В статичном методе мы преобразуем db_cont.cursor.fetchall() (по дефолту являющейся списком кортежей) в список списков,
    наполненных строками, для дальнейших манипуляций, ведь кортеж и тип данных в нем поменять нельзя.


4) ignore_RunTimeError (staticmethod)


    Статичный метод. Избавляет от ошибки, когда мы хотим удалить уже удаленный ранее элемент в последовательности.

5) clear_page


    Метод очистки страницы от всех виджетов (надписей, кнопок, полей ввода и тд). Используется при выборах команд и 
    в самих командах при переходе на новую страницу. Здесь есть нюансы:
    В методе очищается список self.widgets_colletion. Это список, который каждый раз очищается при переходе на новую страницу
    и сразу заполняется текущими виджетами страницы (или виджетом, который мы вызываем на странце текущей). Он создан 
    для того, чтобы сразу избавляться от всех виджетов предыдущей страницы. Через LC вызываем у каждого виджета метод 
    .del_widget(). Позже (через clear) очищаем сам список от остатков, так как могут оставаться ссылки.

6) home_page


      Метод возврата на домашнюю страницу с помощью метода self.home_page(). Его описание будет ниже.

7) messagebox_method

    
    Метод создания всплывающего окна. Импортируется соответствующий класс из файла Widgets.py и создается его экземпляр.
    Параметры метода:
    1) content - текст в окне
    2) content_button - текст в кнопке действия с окном
    3) level_message - уровень сообщения (от этого зависит тип иконки в окне)

8) label_method


    Метод создания статичной надписи. Импортируется соответствующий класс из файла Widgets.py и создается его экземпляр.
    Параметры метода:
    1) right - расположение по оси Х (вправо от верхнего левого угла) 
    2) down - расположение по оси У (вниз от верхней грани)
    3) content - текст надписи

9) button_method


    Метод создания кнопки. Импортируется соответствующий класс из файла Widgets.py и создается его экземпляр.
    Используется метод класса click, который возвращает выполнении функции func, которая закинута на кнопку. 
    Параметры метода:
    1) content - текс в кнопке 
    2) right - расположение по оси Х (вправо от верхнего левого угла) 
    3) down - расположение по оси У (вниз от верхней грани)
    4) size - размер кнопки 
    5) func - функция, выполняемая при нажати на кнопку

10) table_method 
 
   
    Метод создания таблицы. Импортируется соответствующий класс из файла Widgets.py и создается его экземпляр.
    Параметры метода:
    1) data - данные для таблицы. Идут в формате двумерного массива, где каждый подсписок - строка в таблице.

11) search_data_method


    Метод поиска и вывода данных. Параметры метода:
    1) content - текст для надписи
    2) column - имя столбца
    Сначала выбираем, по каким данным будем искать контакт: по имени, номеру или почте.
    Размещаем надпись с вопросом.
    После этого в поле ввода пишем значение, по которому хотим найти контакт.
    Кликаем кнопку "Найти контакт" и тем самым запускаем функцию search()
    В функции search(), согласно имени столбца для поиска (параметр column) осуществляем поиск по соответствующим полям 
    таблицы. При нахождении, обрабатываем резльтаты с помощью метода found_contacts и выводим с ними таблицу, используя
    метод table_method.

12) back_button


    Метод создания кнопки, которая возвращает к списку команд. Используется метод button_method.


13) view_table


    Метод отображения всей таблицы. Выбираем все значение, прогоняем через метод found_contacts и показываем таблицу.
    В методе имеется условие: если id_field == True, то помимо таблицы, мы размещаем на экране поле для ввода id и
    соответствующую надпись. Будет применяться при работе с таблицей. В данном методе, только отображение.
    
## Методы создания и отображения страниц приложения

Каждый метод привязан к определенной команде со стартовой страницы с кнопками. На кнопках висят вызовы соответствующих методов,
прописанных в словаре self.database_methods (мы его создали в начале). Также на кнопках сидят надписи из словаря commands.
В self.database_methods исключением является последняя пара ключ:значение. В ней находится анонимная лямбда функция,
отвечающая за прямой выход из приложения.

14) page_commands


    Основная страница с командами. Нажатие каждой кнопки несет за собой выполнение соответствующего метода создания и 
    отображения страниц в приложении.

15) page_insert 


    Метод добавления данных в таблицу (БД).
    Сначала очищаем страницу.
    Размещаем надпись действия.
    Размещаем три поля для ввода имени, номера и почты.
    Размещаем две кнопки: занести данные в базу и возврат на предыдущую страницу.
    
    insert_database() - непосредственно функция внесения данных в БД
    Cохраняем в переменные три значения, которые мы ввели выше с помощью функции .text()
    Cоздаем из них список
    Дальше условие: если все поля заполнены (дают True).
    Следующее условие, если предыдщее выполняется: если номер и почта, которые ввел пользователь соответствуют паттерну 
    в self.patterns (он возвращает True)
    При выполнении обоих условий вставляем данные в таблицу через .execute() и сохраняем через .commit()
    Очищаем таблицу и выводим надпись об успешном добавлении и добавляем кнопку возврата на главный экран с командами.
    Добавление в таблицу мы проверяем через try-except: добавление будет происзодить только в том случае, если у нас нет
    такого контакта в БД.

    Если условия не выполняются:
    Создаем список с булевыми значениями введенных данных. Если данные введены - True, иначе - else.
    Создаем словарь с ключами от 0 до 2 и соотвественными значениями, в которых находятся методы всплывающих окон об 
    отсутствии данных.
    Запускаем LC по списку с булевыми значениями через функцию enumerate и выводим значение ключа верхнего словаря
    через data[0], если data[1] равно False. Получаем соответствующее окно.

16) page_search_name


    Метод, вызывающий метод page_search_number_mail с параметрами для нахождения контакта по имени. Выделен в отдельный 
    метод для удобства

17) page_search_name


    Метод нахождения контакта по почте или телефону
    Очищаем страницу
    Размещаем надпись с вопросом, по каким данным мы хотим найти контакт.
    Размещаем две кнопки с выбором: искать по номеру или телефону.
    Размещаем кнопку возврата в главное меню.
    При нажатии на кнопку вызывается метод search_data_method с соответствующими параметрами. Метод описан выше в п.10

18) page_update


    Метод обновления данных контакта.
    Очищаем страницу
    Создаем пустой временный список self.temporary для виджетов и self.lines для полей ввода.
    Размещаем всю БД в табличном виде.
    Размещае две кнопки: "Ок" и "Назад". Кнопка "Ок" запускает функция page_update_local, кнопка назад возвращает нас
    на страницу с командами.
    page_update_local - главная функция, в которую мы попадаем после нажатия кнопки "Ок".
    query_update - вспомогательная функция, которая обновляет данные в базе на те, которые подаются ей на вход и выводит
    соответствуюущее сообщение. Данные могут быть равны текущим, если мы их не выбирали для изменения.
    self.id_text - текст, который мы вводим на странице с таблицей в поле ввода id. Текст извлечен из переменной
    self.id_line, который м объявили в методе self.view_table.
    Выбираем строку из БД в соответствии с введенным id, прогоняем через метод self.found_countacts для избавления от
    кортежей.
    Сохраняем это в переменную self.result_data. Если переменная получается пустой - значит мы не ввели id для выбора
    данных. Выводим соответствующее всплывающее окно в этом случае.
    Иначе(если slef.result_data не пустой):
    Очищаем страницу
    Выводим табличным методом данные self.result_data
    Выводим надпись с вопросом о том, как именно мы хотим менять значения: одно, несколько или все?
    Если выбираем "Одно", то запускается функция one_value, несколько - функция some_value,
    все - функция all_value. При переходах среди этих функций и внутри этих функций у нас всегда очищается, а потом
    пересоздается список self.temporary. На каждой странице в фукнциях он хранит виджеты, которые будут исчезать при
    переходе на следующую страницы или переходе назад.

    _________
    one_value - функция, позволяющая изменить одно значение по выбору: имя, номер или почту.
    Очищаем self.temporary и пересоздаем его в методе clear_temporary() (если в нем что то есть)
    Размещаем надпись о том, какое именно значение мы хотим поменять.
    Размещаем три кнопки выбора ОДНОГО значения под изменение через цикл и подвязываем на каждую кнопку свою функцию
    lambda из словаря выше. Каждая функция lambda вызывает функцию line_for_change с соответствующим параметром.
    
    line_for_change - функция изменения ОДНОГО значения
    Очищаем self.temporary и пересоздаем его в методе clear_temporary() (если в нем что то есть)
    Размещаем надпись о введении новых данных. В надписи соответствующий параметр.
    Размещаем поле для введения новыйх данных. Не забываем все добавлять в списки для виджетов.
    Размещаем кнопку для внесения изменений, на которую привязываем функцию change_data
    
    change_data - функция, вызывающая query_update, если все ок.
    сохраняем в переменные текст из поля для ввода выше и данные выбранного пользователя. 
    Дальше проверяем условия:
    если параметр data_change функции line_for_change == 'Имя', то меняем значение имени в данных выбранного контакта на
    новое. После этого запускаем фукнцию query_update.
    query_update - отдельная функция, которая отвечает за обновление базы данных. Создана, чтобы не дублировать код, так
    как конструкция внутри нее будет применяться в нескольких местах. через execute обновляем БД и выводим
    соответствующее всплывающее окно.
    _________

    _________
    all_value - функция, позволяющая изменить все значения. Сначала вызываем метод self.clear_temporary, чтобы без проблем
    Очищаем self.temporary и пересоздаем его в методе clear_temporary() (если в нем что то есть)
    Устанавливаем координату низа верхней (первой) надписи.
    Создаем еще один временный пустой список self.lines для полей ввода (QLineEdit). Он нам понадобится позже.
    Запускаем цикл по названиям столбцов таблицы. Размещаем три поля ввода с соответствующими надписями. Все виджеты не
    не забываем добавлять во временный список self.temporary. Дополнительно добавляем виджеты полей ввода в список 
    self.lines. В течении цикла увеличиваем переменную координаты низа надписей.
    Добавляем кнопку внесения изменений, запускающую функцию change_data

    change_data - функция, вызывающая query_update, если все ок. 
    text_number, text_mail - переменные, в которые мы сохраняем текст номера и почты, введенный ранее в поля. Извлекаем
    его мы из атрибута line с помощью встроенного в него метода .text() по индексу во временном списке self.lines.
    Имя мы не трогаем, так как мы не будем прогонять его через проверку на соответствие регулярному выражению в методе 
    self.patterns.
    Создаем список patterns_ok, в котором будут вызовы метода self.patterns с соответствующими параметрами номера и почты.
    Если оба элемента списка возвращают True (оба значения соответстуют паттерну), то запускаем query_update(). В параметр
    кидаем распакованный list comprehensions с текстом из self.lines. Обновляем данные, коммитим БД и выводим
    соответствующее сообщение.
    _________

    _________
    some_value - функция, позволяющая выбрать, какие данные мы хотим поменять. 
    Очищаем self.temporary и пересоздаем его в методе clear_temporary() (если в нем что то есть)
    Размещаем надпись выбора данных, которые мы хотим поменять. 
    checkbox_down, sself.lines - переменные, отвечающие с координаты н размещения объекта QCheckBox и временны список 
    для полей ввода.
    Запускаем цикл по названиям столбцов.
    На каждой итерации цикла создаем объект QCheckBox (кнопку, которая может быть включена или выключена), называющейся
    именем текущего столбца в цикле. Не забываем добавлять все в self.temporary.
    Размещаем кнопку "Далее", вызывающую фукнцию data_selection

    data_selection - функция, в которой размещаются поля кнопок, которые на прошлой странице были включены. 
    Вводим координату Y размещения поля ввода данных. Запускаем цикл по временному списку self.temporary.
    В цикле ставим условия: 
    1 условие: если виджет на текущей итерации цикла обладает атрибутом checkbox (для этого используем hasattr), т.е.
    является объектом QCheckBox.
    2 условие (проверяется только в случае, когда первое условие возвращает True): если этот виджет
    был включен (кнопка QCheckBox была нажата)
    Если оба условия возвращают True, то сохраняем в переменную название кнопки и размещаем над полем ввода
    Размещаем поле ввода.
    Добавляем в список self.lines подсписок, содержащий имя поля и само поле.
    В течении цикла инкрементируем кординату Y (в переменной down).
    Если после цикла, список self.lines оказывается пустым - это значит, мы никакую кнопку не выбрали. Получаем
    соответствующее всплывающее окно об этом.
    Иначе(если хотя бы одна кнопка была включена): 
    Очищаем self.temporary и пересоздаем его в методе clear_temporary() (если в нем что то есть)
    Сохраняем все элементы списка self.lines в список self.temporary. Список self.lines после этого удаляем. Цель данной
    процедуры в том, чтобы при очистке self.temporary удалялись и поля ввода. В self.lines мы эти поля заносили
    для того, чтобы было удобнее извлекать из них текст. Если бы их сразу внесли в self.temporary, нам бы пришлось
    сначала ставить условие по типу данных, а это - лишний код, от которого мы и избавились.
    размещаем кнопки внесения изменения и возврата на предыдущую страницу.

    При нажатии "Внести изменения" запускается функция change_data. Она уже вызывает query temporary (метод изменения 
    данных), если все ок.
    change_data - функция, которая вызывает query temporary (метод изменения данных), если все ок.
    В начале выводим в отдельное переменную булево значение введенных данных. Если одно не введено, то буде False, так 
    невведенное значение - это пустой строчный объект. Если возвращает False, то выводим всплывающее окно о незаполненных
    полях.
    иначе:
    text_data, contact - пременные, сохраняющие пустой список и выбранные данные из self.result_data без элемента с 
    нулевым индексом (т.е. без номера id). В списке contact далее мы будем менять соответствующие данные и через него 
    менять их в базе.
    
    mutate_contact - впомогательная функция, меняющая элемент по индексу в списке contact.
    mutate_functions - словарь, в котором ключи - имена столбцов выбранного контакта, значения - анонимные лямбда
    функции с параметром data и функцией mutate_contact в выражении. data - параметр, содержащий новые данные.
    Запускаем цикл по временному списку self.temporary.
    Все поля для ввода и их имена содержатся в подсписках временного списка. Ставим условие работы только с подсписками.
    Сохраняем в переменную имя поля (1 элемент подсписка) и текст в поле(2 элемент подсписка)
    Вызываем функцию с в словаре mutate_functions через ключ в нем. Ключ: имя поля. Параметр функции лямбда - 
    текст из поля.
    Происходит изменение соответствующих данных в списке contact.
    Прогоняем данные номера и почты через self.patterns. Если все ок и они соответствуют паттерну регулярных выражений,
    то закидываем распакованный список contact в метод qury_update и производим обновление в БД.
    В противном случае выводим всплывающее окно о несоответствии нужному формату.
    

19) del_page


    Метод удаления контакта.
    Очищаем страницу.
    Размещаем таблицу методом self.view_table с полем для ввода id контакта.
    Размещаем кнопки "удалить", удаляющую контакт, и "назад", вовзращающую к таблице команд на домашнюю страницу.
    
    del_contact - функция удаление контакта по id.
    сохраняем в переменную id контакта, который мы ввели в поле.
    Выбираем всю базу данных
    Выводим все id из преобразованного в self.found_contacts кортежа fetchall. В методе получается список из подсписков,
    состоящих из 4 элементов [id, Имя, Номер, Почта]. Соответственно, выводим нулевые элементы через LC.
    Условие: если id, которые мы ввели содержится в списке id - тогда проводим операцию удаления по этому id
    соответствующего контакта из БД и выводим сообщение об этом. Иначе: выводим сообщение об отсутствии контакта.
20) record_yaml_page


    Метод записи базы данных в файл YAML-формата.
    Выбираем всю базу
    Создаем кортеж данных всей базу
    Создаем словарь контактов с помощью LC по кортежу.
    Открываем на запись файл contacts_file_PYQT5.yaml (или на перезапись, если он существует)
    Через dump закидываем словарь в файл. allow_unicode=True - опция поддержки UTF-8.
    Выводим сообщение об успешном создании файла.

21) load_from_yaml


    Метод выгрузки данных из файла YAML.
    Очищаем страницу.
    Открываем файл 'contacts_file_PYQT5.yaml'
    С помощью load  выгружаем из него данные и сохраняем в словарь.
    Извлекаем первичные значения словаря: словарь структуры { Пользователь id: [данные о контакте] }
    Далее извлекаем ключи из этих первичных значений (Контакт id)
    Из этих ключей извлекаем цифры - номера id контактов.
    Извлекаем данные контактов. Каждый подсписок - это одна строка.
    Соединяем id и данные. Добавляем id на первую позицию в подсписках в dates_users.
    Создаем новый списк id_dates и добавляем в него с помощью цикла обработанные подсписки из dates_users. В обработке
    мы избавляем от лишних слов в данных. Лишнее слова - названия столбцов в строке.
    Закидываем получившийся список с подсисками в метод self.table_method и выводим таблицу с кнопкой "Назад"


22) clear_table


    Метод очистки всей таблицы.
    Очищаем страницу
    Показываем таблицу БЕЗ поля для ввода id (id_field=False)
    Размещаем надпись с вопросом, хотим ли мы очистить таблицу
    Размещаем две кнопки, "Да" и "Назад". "Назад" возвращает нас в меню, "Да" запускает функцию clear()
    В функции получаем предупреждение во всплывающем окне, что таблица будет полностью очищена и кнопки подверждения
    Если соглашаемся (проверяем через условие: если текст нажатой кнопки == 'Да'), то очищаем полностью таблицу по
    условию - удаляем все контакты, у которых первчиный ключ (id) больше нуля
    Потом коммитим
    Потом сбрасываем счетчик primary_key, чтобы при следующем заполнении БД первичный ключи начинались с нуля
    (в противном случае они начинаются со следующего за последним pk значения из удаленной БД)
    Если в окне кликаем на "нет" то окно закрывается и ничего не происходит.
    
23) random_values


    Метод заполнения БД случайными (фейковыми) значениями.
    Очищаем страницу.
    Создаем экземпляр класса Faker с настройками для русского языка. Faker - библотека для генерации фейковых данных.
    Сохраняем в переменную пробел - понадобится при форматировании строк.
    Размещаем надпись с вопросом, сколько случайных контактов мы хотим создать?
    Создаем поле ввода и вносим в него цифру. Размещаем его. Не забываем добавить виджед в общую коллекцию
    Размещаем кнопку "Добавить контакты" для запуска функции instert_random. Размещаем кнопку возврата в главное меню.
    instert_random - функция, генерирующая контакты
    Сохраняем в переменную введенную цифру из поля для ввода.
    Запускаем цикл через обработчик try-except. Если мы, вдруг, в поле для ввода ввели не цифру, то мы получим ошибку 
    ValueError, так как id не может быть чем то, кроме цифры.
    ИНаче: запускаем цикл-счетчик до введенной цифры и с помощью встроенных инструментов Faker создаем пользователей,
    попутно занося их в БД. Если все ок  - коммитим БД и выводим сообщение об успешной генерации.

24) view_page
    

    Метод показа страницы со всей базой данных в табличном виде
    Очищаем страницу
    Показываем таблицу (без поля ввода)
    Размещаем кнопку назад

25) getattr


    Магический метод нам нужен, чтобы без ошибок проходить через проверки self.temporary и self.lines в момент, когда
    они еще не созданы. Без метода мыполучаем ошибку отсутствия этих элементов в памяти.

26) clear_temporary


    Метод для очистки временных списков self.temporary и/или self.lines.
    Внутренняя функция exam_widget имеет тернарный оператор удаления виджетов отдельных и тех, которые находятс в 
    подсписке.
    Если существует self.temporary - прогоняем виджет из него через функцию exam_widget. Затем пересоздаем
    self.temporary.
    Иначе - создаем self.temporary
    Если параметр метода all_list существует - то аналогичную операцию проводим с self.lines.
    
    
    
Проект запускается из своего виртуального окружения.
 