# -*- coding: utf-8 -*-

import os
import sys
import time
from libs.hh_parse import SearchQuery
from libs.hh_config import Data
from libs.hh_mssql import MssqlConnection

class ConsoleApplication:
    
    def __init__(self):
        self.main()

    def menu(self):
        print(u'\nhhparser v1.1. Программа для парсинга сайта https:\hh.ru.')
        print(u'\n-----------------------------------------')
        print(u'1. Поисковый запрос')
        print(u'2. Поисковый запрос из файла')
        print(u'3. Конфигурация программы')
        print(u'4. Проверка подключения к БД')
        print(u'5. Выход')
        print(u'-----------------------------------------\n')

    def main(self):
        while True:
            self.menu()
            cmd = input(u'Введите команду: ')
            if cmd == '1':
                self.cls()
                print(u'\nПравила составления запроса:')
                print(u'''1) Сам запрос или подзапросы необходимо выделять ковычками, например "SQL" или 'SQL'.''')
                print(u'2) Доступные операторы над подзапросами: "&" - ПЕРЕСЕЧЕНИЕ, "+" - ОБЪЕДИНЕНИЕ, "/" - РАЗНОСТЬ.')
                print(u'3) Можно использовать скобки, например ("ит" + "ИТ" + "IT") & "SQL".')
                print(u'4) Допускать ошибки в составлении запроса не рекомендуется.')
                search_text = input(u'\nПоисковый запрос: ')
                query = Query(search_text)
                query.run()
            elif cmd == '2':
                self.cls()
                print(u'Если файл находится в папке с программой, то путь до файла не обязателен.')
                print(u'В противном случае необходимо указать полный путь до файла.\n')
                filepath = input(u'Введите путь до файла: ')
                query = QueryFile(filepath)
                query.run()
            elif cmd == '3':
                self.cls()
                self.configuration()
            elif cmd == '4':
                self.cls()
                self.check_connection()
            elif cmd == '5':
                self.exit()
            else:
                self.cls()
                print(u'\nНеверная команда, попробуйте еще раз!\n')

    def db_add_qustion(self):
        while True:
            q_text = input(u'\nХотите добавить в базу данных?(y/n): ')
            if q_text == 'y':
                return 1
            elif q_text == 'n':
                return 0
            else:
                print(u'Неправильный ввод!')

    def check_connection(self):
        config = Data()
        config.load_from_conf()
        conn = MssqlConnection(config.rserver_name(), config.rdb_name(), config.rusername(), config.rpassword())
        print('Установка соединения с БД...\n')
        check = conn.check_connection()
        if check == 1:
            print(u'Сообщение: Соединение с базой установлено!')
        else:
            print(u'Сообщение: Соединение с базой не установлено!')

    def configuration(self):
        config = Data()
        config.load_from_conf()
        print(u'\nКонфигурационный файл config.ini.')
        print(u'\n-----------------------------------------')
        print(u'\nИмя сервера: ', config.rserver_name())
        print(u'Имя базы данных: ', config.rdb_name())
        print(u'Имя пользователя: ', config.rusername())
        print(u'Пароль: ', config.rpassword())
        print(u'Тайм-аут между запросами: ', config.rtimeout())
        print(u'Требования:')
        print(config.rrequirments())
        print(u'Условия:')
        print(config.rconditions())
        print(u'Ожидания:')
        print(config.rexpectations())
        print(u'\n-----------------------------------------')

    def cls(self):
        os.system('cls')

    def exit(self):
        sys.exit()

class Query(ConsoleApplication):
    def __init__(self, search_text):
        self.search_text = search_text

    def run(self):
        #SearchQuery
        self.stats = Stats()
        self.config = Data()
        self.config.load_from_conf()
        try:
            self.stats.search_time_start_func()
            self.query_object = SearchQuery()
            self.query_object.vacancy_count_signal.connect(self.stats.vacancy_count)
            self.query_object.vacancy_analized_signal.connect(self.stats.vacancy_analized)
            self.query_object.query_finished_signal.connect(self.stats.search_time_end_func)
            self.query_object.query_finished_signal.connect(self.add_into_database)
            self.query_object.set_query_config(self.search_text, self.config.rtimeout(), self.config.rrequirments(), self.config.rexpectations(), self.config.rconditions())
            self.query_object.start_search()
            self.query_object.get_vacancy_information(self.stats.rsearch_time_start())
        except Exception as inst:
            self.cls()
            print(u'\nСообщение:', inst)
        except:
            print(u'\nСообщение: Непредвиденная ошибка, выполнение запроса будет остановлено!')

    def add_into_database(self):
        self.stats.search_time_print()
        conn = MssqlConnection(self.config.rserver_name(), self.config.rdb_name(), self.config.rusername(), self.config.rpassword())
        ans = self.db_add_qustion()
        if ans == 1:
            conn_result = conn.check_connection()
            if conn_result == 1:
                try:
                    conn.insert_all_data(self.query_object)
                    print(u'Добавление успешно завершено.')
                except Exception as inst:
                    self.cls()
                    print(u'\nСообщение:', inst)
                except:
                    self.cls()
                    print(u'\nСообщение: Непредвиденная ошибка')
            else:
                self.cls()
                print(u'\nСоединение с базой не установлено.')
        else:
            self.cls()
            print(u'\nОперация добавления отменена.')

class QueryFile(ConsoleApplication):

    def __init__(self, filepath):
        self.filepath = filepath

    def run(self):
        #File SearchQuery
        self.config = Data()
        self.config.load_from_conf()
        try:
            self.queries_names = self.open_file()
        except:
            self.cls()
            print(u'\nНевозможно открыть файл.')
            return
        self.queries = []
        for query in self.queries_names:
            try:
                print(u'\nОбработка запроса : {0}'.format(query))
                self.stats = Stats()
                self.stats.search_time_start_func()
                self.query_object = SearchQuery()
                self.query_object.vacancy_count_signal.connect(self.stats.vacancy_count)
                self.query_object.vacancy_analized_signal.connect(self.stats.vacancy_analized)
                self.query_object.query_finished_signal.connect(self.stats.search_time_end_func)
                self.query_object.query_finished_signal.connect(self.add_into_list)
                self.query_object.set_query_config(query, self.config.rtimeout(), self.config.rrequirments(), self.config.rexpectations(), self.config.rconditions())
                self.query_object.start_search()
                self.query_object.get_vacancy_information(self.stats.rsearch_time_start())
                self.stats.search_time_print()
            except Exception as inst:
                print(u'Сообщение:', inst)
            except:
                print(u'Сообщение: Непредвиденная ошибка, выполнение запроса будет остановлено!')
        if self.queries:
            self.add_into_database()
        else:
            print(u'\nНету данных для добавления в базу данных!')

    def open_file(self):
        file = open(self.filepath)
        queries_names = []
        for line in file:
            queries_names.append(line)
        return queries_names

    def add_into_database(self):
        conn = MssqlConnection(self.config.rserver_name(), self.config.rdb_name(), self.config.rusername(), self.config.rpassword())
        ans = self.db_add_qustion()
        if ans == 1:
            conn_result = conn.check_connection()
            if conn_result == 1:
                try:
                    for query in self.queries:
                        print(u'Добавление {0} в базу данных.'.format(query.search_text))
                        conn.insert_all_data(query)
                    print(u'Добавление успешно завершено.')
                except Exception as inst:
                    self.cls()
                    print('\nСообщение:', inst)
                except:
                    self.cls()
                    print('\nСообщение: Непредвиденная ошибка')
            else:
                self.cls()
                print('\nСоединение с базой не установлено.')
        else:
            self.cls()
            print(u'\nОперация добавления отменена.')        

    def add_into_list(self):
        self.queries.append(self.query_object)

class Stats:
    def __init__(self):
        self.search_time_start = 0
        self.search_time = 0

    def rsearch_time_start(self):
        return self.search_time_start

    def vacancy_count(self, value):
        self.vacancy_count = value
        print(u'Было найдено ', value, ' вакансий.')
    
    def vacancy_analized(self, value):
        self.vacancy_analized = value
        prog = int((self.vacancy_analized / self.vacancy_count)*100)
        print(u'Обработка данных выполнена на {0}%\r'.format(prog), end='')
    
    def search_time_start_func(self):
        self.search_time_start = time.time()
    
    def search_time_end_func(self):
        self.search_time = int(time.time() - self.search_time_start)

    def search_time_print(self):
        print(u'\nПоиск и обработка вакансий длились ', self.search_time, ' секунд.') 

if __name__ == '__main__':
    app = ConsoleApplication()
