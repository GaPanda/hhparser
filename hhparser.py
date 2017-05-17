# -*- coding: utf-8 -*-

import os
import sys
import time
import libs.hh_parse as hh_parse
import libs.hh_config as hh_config
import libs.hh_mssql as hh_mssql

def menu():
    print(u'\nhhparser v1.1. Программа для парсинга сайта https:\hh.ru.')
    print(u'\n-----------------------------------------')
    print(u'1. Поисковый запрос')
    print(u'2. Поисковый запрос из файла')
    print(u'3. Конфигурация программы')
    print(u'4. Проверка подключения к БД')
    print(u'5. Выход')
    print(u'-----------------------------------------\n')

def main():
    config = hh_config.data()
    config.load_from_conf()
    while True:
        menu()
        cmd = input(u'Введите команду: ')
        if cmd == '1':
            cls()
            print(u'\nПравила составления запроса:')
            print(u'''1) Сам запрос или подзапросы необходимо выделять ковычками, например "SQL" или 'SQL'.''')
            print(u'2) Доступные операторы над подзапросами: "&" - ПЕРЕСЕЧЕНИЕ, "+" - ОБЪЕДИНЕНИЕ, "/" - РАЗНОСТЬ.')
            print(u'3) Можно использовать скобки, например ("ит" + "ИТ" + "IT") & "SQL".')
            print(u'4) Допускать ошибки в составлении запроса не рекомендуется.')
            start_query(config)
        elif cmd == '2':
            cls()
            print(u'Если файл находится в папке с программой, то путь до файла не обязателен.')
            print(u'В противном случае необходимо указать полный путь до файла.\n')
            filepath = input(u'Введите путь до файла: ')
            start_file_query(filepath, config)
        elif cmd == '3':
            cls()
            configuration(config)
        elif cmd == '4':
            cls()
            check_connection(config.rserver_name(), config.rdb_name())
        elif cmd == '5':
            exit()
        else:
            cls()
            print(u'\nНеверная команда, попробуйте еще раз!\n')

def start_query(config):
    #SearchQuery
    search_text = input(u'\nПоисковый запрос: ')
    query_class = hh_parse.SearchQuery(search_text)
    query_class.start_search()
    query_class.get_vacancy_information(config.rrequirments(), config.rconditions(), config.rexpectations())
    query_class.end_of_search()
    ans = db_add_qustion()
    insert_into_db(config.rserver_name(), config.rdb_name(), query_class, ans)

def start_file_query(filepath, config):
    #File SearchQuery
    queries_names = []
    queries = []
    file = open(filepath)
    for line in file:
        queries_names.append(line)
    for query in queries_names:
        print('Выполнение запроса ' + query, end = '')
        query_class = hh_parse.SearchQuery(query)
        query_class.start_search()
        queries.append(query_class)
    for query in queries:
        query.get_vacancy_information(config.rrequirments(), config.rconditions(), config.rexpectations())
        query.end_of_search()
    ans = db_add_qustion()
    for key in queries:
        insert_into_db(config.rserver_name(), config.rdb_name(), key, ans)

def format_string(string):
    temp = string.split("'")
    temp2 = ''
    for key in temp:
        temp2 += key
    return temp2

def db_add_qustion():
    while True:
        q_text = input(u'\nХотите добавить в базу данных?(y/n): ')
        if q_text == 'y':
            return 1
        elif q_text == 'n':
            return 0
        else:
            print(u'Неправильный ввод!')

def check_connection(server_name, db_name):
    conn = hh_mssql.MSSQLConnection(server_name, db_name)
    print('Установка соединения с БД...\n')
    check = conn.check_connection()
    if check == 1:
        print('Соединение с базой установлено!')
    else:
        print('Соединение с базой не установлено!')
        
def insert_into_db(server_name, db_name, query, ans):
    conn = hh_mssql.MSSQLConnection(server_name, db_name)
    conn_result = conn.check_connection()
    if (query.vacancy_list != []) & (conn_result == 1):
        if ans == 1:
            start = time.time()
            i = 0
            print(u'\nДобавление в БД...')
            id_vacancy = 0
            id_query = conn.insert_query(query.search_text, query.search_time)
            for key in query.vacancy_list:
                try:
                    id_vacancy = conn.insert_vacancy(key.vacancy_name, key.vacancy_company, key.vacancy_salary, 
                    key.currency, key.vacancy_city, key.vacancy_metro, key.vacancy_experience,
                    key.vacancy_date, key.vacancy_url)
                    for c_key in key.conditions_list:
                        id_con = conn.insert_text_condition(format_string(c_key))
                        conn.insert_vac_con(id_vacancy, id_con)
                    for e_key in key.expectations_list:
                        id_exp = conn.insert_text_expectation(format_string(e_key))
                        conn.insert_vac_exp(id_vacancy, id_exp)
                    for r_key in key.requirments_list:
                        id_req = conn.insert_text_requerments(format_string(r_key))
                        conn.insert_vac_req(id_vacancy, id_req)
                    conn.insert_query_vacancy(id_vacancy, id_query)
                except:
                    conn.delete_after_error(id_vacancy)
                i += 1
            finish = time.time() - start
            print(u'\nДобавление вакансий в базу длилось ', finish, ' секунд.')
            os.system("pause")
            os.system('cls')
        elif ans == 0:
            os.system('cls')
            print(u'\nОперация добавления отменена!')
        else:
            print(u'Ошибка!')
    elif (query.vacancy_list != []) & (conn_result == 0):
        os.system('cls')
        print(u'\nСоединение с базой не установлено!')

def configuration(config):
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

def cls():
    os.system('cls')

def exit():
    sys.exit()

if __name__ == '__main__':
    main()
