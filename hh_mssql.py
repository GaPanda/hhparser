import pyodbc

class MSSQLConnection:
    def __init__(self, server_name, db_name):
        self.connection_string = 'DRIVER={SQL Server};SERVER=' + server_name + ';DATABASE=' + db_name + ';'
    
    def insert_name_query(self, name_query):
        '''Добавление текста запроса в таблицу Query_name'''
        conn = pyodbc.connect(self.connetion_string)
        cursor = conn.cursor()
        cursor.execute('insert into Query_name(name_query) values (' + name_query + ')')
        cnxn.commit()