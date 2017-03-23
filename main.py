import hh_parse
import os,sys

class data:
    def __init__(self):
        pass
        
def menu():
    print('\nПрограмма для парсинга сайта https:\hh.ru')
    print('\n-----------------------------------------')
    print('1. Поисковый запрос')
    print('2. Конфигурация программы')
    print('3. Выход')
    print('-----------------------------------------\n')

def input_cmd():
    while True:
        menu()
        cmd = input('Введите команду: ')
        if cmd == '1':
            start_query()
        elif cmd == '2':
            pass
        elif cmd == '3':
            exit()
        else:
            print('Неверная команда, попробуйте еще раз!\n')

def start_query():
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

def cls():
    os.system('cls')

def exit():
    sys.exit(0)

def main():
    input_cmd()

if __name__ == '__main__':
    main()