# -*- coding: utf-8 -*-

import libs.hh_parse as hh_parse
import os,sys
import libs.hh_config as hh_config

def menu():
    print(u'\nhhparser v0.1. Программа для парсинга сайта https:\hh.ru')
    print(u'\n-----------------------------------------')
    print(u'1. Поисковый запрос')
    print(u'2. Конфигурация программы')
    print(u'3. Выход')
    print(u'-----------------------------------------\n')

def main():
    config = hh_config.data()
    config.load_from_conf()
    while True:
        menu()
        cmd = input(u'Введите команду: ')
        if cmd == '1':
            start_query(config)
        elif cmd == '2':
            configuration(config)
        elif cmd == '3':
            exit()
        else:
            print(u'Неверная команда, попробуйте еще раз!\n')

def start_query(config):
    #SearchQuery
    search_text = input(u'\nПоисковый запрос: ')
    Query = hh_parse.SearchQuery(search_text)
    Query.start_search()
    Query.get_vacancy_information(config.rrequirments(), config.rconditions(), config.rexpectations())
    Query.end_of_search()
    Query.insert_into_db(config.rserver_name(), config.rdb_name())

def configuration(config):
    cls()
    #Information about config.ini
    print(u'\nКонфигурационный файл config.ini.')
    print(u'\n-----------------------------------------')
    print(u'\nИмя сервера: ', config.rserver_name())
    print(u'Имя базы данных: ', config.rdb_name())
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