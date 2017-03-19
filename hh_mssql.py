import pyodbc

class MSSQLConnection:
    def __init__(self, server_name, db_name):
        self.connection_string = 'DRIVER={SQL Server};SERVER=' + server_name + ';DATABASE=' + db_name + ';'
    
    def insert_name_query(self, name_query):
        '''Добавление записи в таблицу Query_name'''
        conn = pyodbc.connect(self.connection_string)
        try:
            cursor = conn.cursor()
            cursor.execute("insert into Query_name(name_query) values ('" + name_query + "')")
            conn.commit()
        except:
            print('Не удалось добавить имя запроса в БД!')
        finally:
            conn.close()
    
    def insert_name_company(self, name_company):
        '''Добавление записи в таблицу Company'''
        conn = pyodbc.connect(self.connection_string)
        try:
            cursor = conn.cursor()
            cursor.execute("insert into Company(name_company) values ('" + name_company + "')")
            conn.commit()
        except:
            print('Не удалось добавить имя запроса в БД!')
        finally:
            conn.close()
    
    def insert_name_vacancy(self, name_vacancy):
        '''Добавление записи в таблицу Name_vacancy'''
        conn = pyodbc.connect(self.connection_string)
        try:
            cursor = conn.cursor()
            cursor.execute("insert into Name_vacancy(name_vacancy) values ('" + name_vacancy + "')")
            conn.commit()
        except:
            print('Не удалось добавить имя запроса в БД!')
        finally:
            conn.close()
    
    def insert_name_currency(self, name_currency):
        '''Добавление записи в таблицу Currency'''
        conn = pyodbc.connect(self.connection_string)
        try:
            cursor = conn.cursor()
            cursor.execute("insert into Currency(name_currency) values ('" + name_currency + "')")
            conn.commit()
        except:
            print('Не удалось добавить имя запроса в БД!')
        finally:
            conn.close()

    def insert_name_city(self, name_city):
        '''Добавление записи в таблицу City'''
        conn = pyodbc.connect(self.connection_string)
        try:
            cursor = conn.cursor()
            cursor.execute("insert into City(name_city) values ('" + name_city + "')")
            conn.commit()
        except:
            print('Не удалось добавить имя запроса в БД!')
        finally:
            conn.close()

    def insert_name_metro(self, name_metro):
        '''Добавление записи в таблицу Metro'''
        conn = pyodbc.connect(self.connection_string)
        try:
            cursor = conn.cursor()
            cursor.execute("insert into Metro_station(name_metro_station) values ('" + name_metro + "')")
            conn.commit()
        except:
            print('Не удалось добавить имя запроса в БД!')
        finally:
            conn.close()
    