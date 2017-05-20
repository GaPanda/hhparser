# -*- coding: utf-8 -*-

import os
import sys
import time
from PyQt5.QtCore import QTimer
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
                self.start_query()
            elif cmd == '2':
                self.cls()
                print(u'Если файл находится в папке с программой, то путь до файла не обязателен.')
                print(u'В противном случае необходимо указать полный путь до файла.\n')
                self.start_file_query()
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

    def start_query(self):
        #SearchQuery
        config = Data()
        config.load_from_conf()
        conn = MssqlConnection(config.rserver_name(), config.rdb_name())
        try:
            search_text = input(u'\nПоисковый запрос: ')
            query_object = SearchQuery(search_text, config.rtimeout(), config.rrequirments(), config.rexpectations(), config.rconditions())
            query_object.start_search()
            query_object.get_vacancy_information()
            query_object.end_of_search()
            ans = self.db_add_qustion()
            if ans == 1:
                conn_result = conn.check_connection()
                if (query_object.vacancy_list != []) & (conn_result == 1):
                    conn.insert_all_data(query_object)
                elif (query_object.vacancy_list != []) & (conn_result == 0):
                    print('\nСоединение с базой не установлено.')
            else:
                print(u'\nОперация добавления отменена.')
        except Exception as inst:
            self.cls()
            print('\nСообщение:', inst)
        except:
            print('\nСообщение: Непредвиденная ошибка, выполнение запроса будет остановлено!')

    def start_file_query(self):
        #File SearchQuery
        config = Data()
        config.load_from_conf()
        conn = MssqlConnection(config.rserver_name(), config.rdb_name())
        filepath = input(u'Введите путь до файла: ')
        try:
            queries_names = []
            queries = []
            file = open(filepath)
            for line in file:
                queries_names.append(line)
            for query in queries_names:
                print('Выполнение запроса ' + query, end = '')
                query_object = SearchQuery(query, config.rtimeout(), config.rrequirments(), config.rexpectations(), config.rconditions())
                query_object.start_search()
                queries.append(query_object)
            for query in queries:
                query.get_vacancy_information()
                query.end_of_search()
            ans = self.db_add_qustion()
            if ans == 1:
                conn_result = conn.check_connection()
                if (query_class.vacancy_list != []) & (conn_result == 1):        
                    for key in queries:
                        conn.insert_all_data(key)
                elif (query_class.vacancy_list != []) & (conn_result == 0):
                    self.cls()
                    print('\nСообщение: Соединение с базой не установлено.')
        except Exception as inst:
            self.cls()
            print('\nСообщение:', inst)
        except:
            print('\nСообщение: Непредвиденная ошибка, выполнение запроса будет остановлено!')

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
        conn = MssqlConnection(config.rserver_name(), config.rdb_name())
        print('Установка соединения с БД...\n')
        check = conn.check_connection()
        if check == 1:
            print('Сообщение: Соединение с базой установлено!')
        else:
            print('Сообщение: Соединение с базой не установлено!')

    def configuration(self):
        config = Data()
        config.load_from_conf()
        print(u'\nКонфигурационный файл config.ini.')
        print(u'\n-----------------------------------------')
        print(u'\nИмя сервера: ', config.rserver_name())
        print(u'Имя базы данных: ', config.rdb_name())
        print(u'Имя пользователя: ', config.rusername())
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

if __name__ == '__main__':
    app = ConsoleApplication()
