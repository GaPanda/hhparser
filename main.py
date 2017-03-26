import hh_parse
import os,sys
import hh_config

def menu():
    print('\nhhparser v0.1. Программа для парсинга сайта https:\hh.ru')
    print('\n-----------------------------------------')
    print('1. Поисковый запрос')
    print('2. Конфигурация программы')
    print('3. Выход')
    print('-----------------------------------------\n')

def main():
    config = hh_config.data()
    config.load_from_conf()
    while True:
        menu()
        cmd = input('Введите команду: ')
        if cmd == '1':
            start_query(config)
        elif cmd == '2':
            configuration(config)
        elif cmd == '3':
            exit()
        else:
            print('Неверная команда, попробуйте еще раз!\n')

def start_query(config):
    #Server name
    server_name = 'DESKTOP\SQLEXPRESS'
    #Database name
    db_name = 'hh'
    #SearchQuery
    search_text = input('\nПоисковый запрос: ')
    Query = hh_parse.SearchQuery(search_text)
    Query.start_search()
    Query.get_vacancy_information()
    Query.end_of_search()
    Query.insert_into_db(server_name, db_name)

def configuration(config):
    #Information about config.ini
    print('Имя сервера: ', config.rserver_name())
    print('Имя базы данных: ', config.rdb_name())
    print('Тайм-аут между запросами: ', config.rtimeout())
    print(config.rrequirments())
    print(config.rconditions())
    print(config.rexpectations())

def cls():
    os.system('cls')

def exit():
    sys.exit()

if __name__ == '__main__':
    main()