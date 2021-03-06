import pyodbc

class MssqlConnection:
    def __init__(self, server_name, db_name, username, password):
        self.connection_string = 'DRIVER={SQL Server};SERVER=' + server_name + ';DATABASE=' + db_name + ';UID=' + username + ';PWD=' + password

    def check_connection(self):
        try:
            conn = pyodbc.connect(self.connection_string)
            conn.close()
            return 1
        except:
            return 0

    def queries_show(self):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        queries = cursor.execute('EXEC QUERIES')
        return queries

    def vacancies_show(self, value):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        vacancies = cursor.execute('EXEC VACANCIES ' + str(value))
        return vacancies

    def vacancy_show(self, value):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        cursor.execute('EXEC VACANCY_PROC ' + str(value))
        vacancy = cursor.fetchone()
        return vacancy

    def vacancy_show_error(self, value):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        cursor.execute('EXEC VACANCY_ERROR_PROC ' + str(value))
        vacancy = cursor.fetchone()
        return vacancy

    def vacancy_show_location(self, value):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        cursor.execute('EXEC LOCATION_PROC ' + str(value))
        vacancy_location = cursor.fetchone()
        return vacancy_location

    def vacancy_show_req(self, value):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        vacancy_req = cursor.execute('EXEC REQUERMENTS_PROC ' + str(value))
        return vacancy_req

    def vacancy_show_exp(self, value):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        vacancy_exp = cursor.execute('EXEC EXPECTATIONS_PROC ' + str(value))
        return vacancy_exp

    def vacancy_show_con(self, value):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        vacancy_con = cursor.execute('EXEC CONDITIONS_PROC ' + str(value))
        return vacancy_con

    def format_string(self, string):
        temp = string.split("'")
        temp2 = ''
        for key in temp:
            temp2 += key
        return temp2

    def insert_all_data(self, query):
        i = 0
        id_vacancy = 0
        id_query = self.insert_query(query.search_text, query.search_time)
        for key in query.vacancy_list:
            try:
                id_vacancy = self.insert_vacancy(key.vacancy_name, key.vacancy_company, key.vacancy_salary, 
                key.currency, key.vacancy_city, key.vacancy_metro, key.vacancy_experience,
                key.vacancy_date, key.vacancy_url)
                for c_key in key.conditions_list:
                    id_con = self.insert_text_condition(self.format_string(c_key))
                    self.insert_vac_con(id_vacancy, id_con)
                for e_key in key.expectations_list:
                    id_exp = self.insert_text_expectation(self.format_string(e_key))
                    self.insert_vac_exp(id_vacancy, id_exp)
                for r_key in key.requirments_list:
                    id_req = self.insert_text_requerments(self.format_string(r_key))
                    self.insert_vac_req(id_vacancy, id_req)
                self.insert_query_vacancy(id_vacancy, id_query)
            except:
                self.delete_after_error(id_vacancy)
            i += 1
        
    def insert_unique_value(self, value_in, table_info):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        value = value_in.__str__()
        try:
            cursor.execute("insert into " + table_info[0] + "(" + table_info[2] + ") values ('" + value + "')")
            conn.commit()
        finally:
            cursor.execute("select " + table_info[1] + " from " + table_info[0] + " where " + table_info[2] + " = '" + value + "'")
            row = cursor.fetchone()
            conn.close()
            return row[0]

    def insert_m_m_value(self, id_1, id_2, table_info):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        id_1_str = id_1.__str__()
        id_2_str = id_2.__str__()
        try:
            cursor.execute("select " + table_info[1] + " from " + table_info[0] + " where " + table_info[2] + "=" + id_1_str + " and " + table_info[3] + "=" + id_2_str)
            row = cursor.fetchone()
            if row == None:
                cursor.execute("insert into " + table_info[0] + "("\
                + table_info[2] + ", " + table_info[3] + ") values ("\
                + id_1_str + "," + id_2_str + ")")
                conn.commit()
        finally:
            cursor.execute("select " + table_info[1] + " from " + table_info[0] + " where " + table_info[2] + "=" + id_1_str + " and " + table_info[3] + "=" + id_2_str)
            row = cursor.fetchone()
            conn.close()
            return row[0]

    def insert_query(self, name_query, search_time):
        id_query_name = self.insert_query_name(name_query)
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        try:
            cursor.execute("insert into Query (id_query_name, time_analyze_query) values ("+ id_query_name.__str__() + "," + search_time.__str__() +")")
            conn.commit()
        finally:
            cursor.execute("SELECT @@IDENTITY")
            row = cursor.fetchone()
            conn.close()
            return row[0]

    def insert_vacancy(self, n_v, n_c, sal, cur, city, metro, exp, date_vacancy, url_vacancy):
        id_name_vacancy = self.insert_name_vacancy(n_v)
        id_company = self.insert_name_company(n_c)
        print(cur)
        if sal != 'NULL':
            id_currency = self.insert_name_currency(cur)
            id_salary = self.insert_salary(sal, id_currency)
        else:
            id_salary = 'NULL'
        id_experience = self.insert_experience(exp)
        id_city = self.insert_name_city(city)
        id_metro = self.insert_name_metro_station(metro)
        id_location = self.insert_location(id_city, id_metro)
        if date_vacancy != 'NULL':
            date_vacancy = "'" + date_vacancy + "'"
        else:
            date_vacancy = 'NULL'
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        try:
            cursor.execute("insert into Vacancy (id_name_vacancy, id_company, id_salary, id_experience,"\
                + "id_location, date_vacancy, url_vacancy) values (" + id_name_vacancy.__str__() + "," + id_company.__str__()\
                + "," + id_salary.__str__() + "," + id_experience.__str__() + "," + id_location.__str__()\
                +"," + date_vacancy + ",'" + url_vacancy +"')")
            conn.commit()
        finally:
            cursor.execute("select id_vacancy from Vacancy where url_vacancy = '" + url_vacancy + "'")
            row = cursor.fetchone()
            conn.close()
            return row[0]

    def delete_after_error(self, id_vacancy):
        id_v = id_vacancy.__str__()
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        try:
            cursor.execute("delete from Vacancy where id_vacancy=" + id_v)
            conn.commit()
        finally:
            conn.close()

    def insert_query_name(self, value):
        table_info = ['Query_name', 'id_query_name', 'name_query']
        id_r = self.insert_unique_value(value, table_info)
        return id_r

    def insert_name_vacancy(self, value):
        table_info = ['Name_vacancy', 'id_name_vacancy', 'name_vacancy']
        id_r = self.insert_unique_value(value, table_info)
        return id_r
      
    def insert_name_currency(self, value):
        table_info = ['Currency', 'id_currency', 'name_currency']
        id_r = self.insert_unique_value(value, table_info)
        return id_r

    def insert_name_city(self, value):
        table_info = ['City', 'id_city', 'name_city']
        id_r = self.insert_unique_value(value, table_info)
        return id_r

    def insert_name_metro_station(self, value):
        table_info = ['Metro_station', 'id_metro_station', 'name_metro_station']
        id_r = self.insert_unique_value(value, table_info)
        return id_r

    def insert_name_company(self, value):
        table_info = ['Company', 'id_company', 'name_company']
        id_r = self.insert_unique_value(value, table_info)
        return id_r

    def insert_text_condition(self, value):
        table_info = ['Conditions', 'id_condition', 'text_condition']
        id_r = self.insert_unique_value(value, table_info)
        return id_r

    def insert_experience(self, value):
        table_info = ['Experience', 'id_experience', 'text_experience']
        id_r = self.insert_unique_value(value, table_info)
        return id_r

    def insert_text_expectation(self, value):
        table_info = ['Expectations', 'id_expectation', 'text_expectation']
        id_r = self.insert_unique_value(value, table_info)
        return id_r

    def insert_text_requerments(self, value):
        table_info = ['Requerments', 'id_requerment', 'text_requerment']
        id_r = self.insert_unique_value(value, table_info)
        return id_r

    def insert_vac_con(self, id_1, id_2):
        table_info = ['Vac_con', 'id_desc_con', 'id_vacancy', 'id_condition']
        self.insert_m_m_value(id_1, id_2, table_info)

    def insert_vac_exp(self, id_1, id_2):
        table_info = ['Vac_exp', 'id_desc_exp', 'id_vacancy', 'id_expectation']
        self.insert_m_m_value(id_1, id_2, table_info)

    def insert_vac_req(self, id_1, id_2):
        table_info = ['Vac_req', 'id_desc_req', 'id_vacancy', 'id_requerment']
        self.insert_m_m_value(id_1, id_2, table_info)

    def insert_query_vacancy(self, id_1, id_2):
        table_info = ['Query_vacancy', 'id_query_vacancy', 'id_vacancy', 'id_query']
        id_r = self.insert_m_m_value(id_1, id_2, table_info)
        return id_r
    
    def insert_location(self, id_1, id_2):
        table_info = ['Location', 'id_location', 'id_city', 'id_metro_station']
        id_r = self.insert_m_m_value(id_1, id_2, table_info)
        return id_r

    def insert_salary(self, value, currency):
        table_info = ['Salary', 'id_salary', 'salary', 'id_currency']
        id_r = self.insert_m_m_value(value, currency, table_info)
        return id_r