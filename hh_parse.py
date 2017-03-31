# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import re, sys, time
from bs4 import BeautifulSoup
import hh_mssql

URL = "https://spb.hh.ru"
TIMEOUT = 0

def get_html(url):
    '''Получение кода страницы'''
    #Timeout при запросе
    time.sleep(TIMEOUT)
    page = urllib.request.urlopen(url)
    return page.read()

class Vacancy:
    '''Класс описывающий вакансию'''
    def __init__(self, url):
        self.vacancy_url = url
        self.requirments_list = []
        self.conditions_list = []
        self.expectations_list = []

    def search_on_page(self):
        '''Поиск данных на странице вакансии'''
        page = get_html(self.vacancy_url)
        soup = BeautifulSoup(page, 'lxml')
        self.vacancy_name = soup.find(
            'h1', class_="title b-vacancy-title").get_text()
        self.vacancy_company = soup.find(
            'div', class_="companyname").get_text()
        self.vacancy_salary = soup.find('td', class_="l-content-colum-1 b-v-info-content").find(
            'div', class_="l-paddings").get_text()

        try:
            self.vacancy_salary = soup.find('td', class_="l-content-colum-1 b-v-info-content").find(
            'meta', itemprop = "baseSalary").get('content')
            self.currency = soup.find('td', class_="l-content-colum-1 b-v-info-content").find(
            'meta', itemprop = "salaryCurrency").get('content')
        except:
            self.vacancy_salary = "NULL"
            self.currency = "NULL" 
        try:
            self.vacancy_date = soup.find('time', class_="vacancy-sidebar__publication-date").get('datetime')[:10]
        except:
            self.vacancy_date = "NULL"

        vacancy_city_temp = soup.find('td', class_="l-content-colum-2 b-v-info-content").find(
            'div', class_="l-paddings").get_text().split(',')
        self.vacancy_city = vacancy_city_temp[0].strip()
        try:
            self.vacancy_metro = vacancy_city_temp[1]
        except:
            self.vacancy_metro = "Отсутствует информация"

        self.vacancy_experience = soup.find('td', class_="l-content-colum-3 b-v-info-content").find(
            'div', class_="l-paddings").get_text()
        self.vacancy_description = soup.find(
            'div', class_="b-vacancy-desc-wrapper")

    def description_parse(self, requirments, conditions, expectations):
        requirments_list = requirments
        conditions_list = conditions
        expectations_list = expectations
        tag_text = self.vacancy_description.find_all(['strong', 'ul'])
        i = 0
        for key in tag_text:
            if key.get_text().strip() in requirments_list:
                self.requirments_list = self.tag_text_analyze(tag_text, i + 1)
                i += 1
            elif key.get_text().strip() in conditions_list:
                self.conditions_list = self.tag_text_analyze(tag_text, i + 1)
                i += 1
            elif key.get_text().strip() in expectations_list:
                self.expectations_list = self.tag_text_analyze(tag_text, i + 1)
                i += 1
            else:
                i += 1
                continue

    def tag_text_analyze(self, list, position):
        temp_list = []
        for i in range(position, len(list)):
            if list[i].name == 'ul':
                temp_list.append(list[i])
            else:
                break
        if temp_list is not None:
            temp_list = self.temp_list_format(temp_list)
        return temp_list

    def temp_list_format(self, temp_list):
        temp = []
        result = []
        for key in temp_list:
            temp.append(key.find_all('li'))
        for i in temp:
            for j in i:
                temp_j = j.get_text().strip()
                result.append(temp_j)
        return result

    def print_result(self):
        print('Должность: ', self.vacancy_name,
              '\nURL: ', self.vacancy_url,
              '\nДата публикации: ', self.vacancy_date,
              '\nИмя компании: ', self.vacancy_company,
              '\nЗарплата: ', self.vacancy_salary, self.currency,
              '\nОпыт: ', self.vacancy_experience,
              '\nГород: ', self.vacancy_city,
              '\nСтация метро: ', self.vacancy_metro
              )
        if self.requirments_list:
            print('Требования:')
            for key in self.requirments_list:
                print('-', key)
        else:
            print('Требований не найдено!')
        if self.expectations_list:
            print('Ожидания:')
            for key in self.expectations_list:
                print('-', key)
        else:
            print('Ожиданий не найдено!')        
        if self.conditions_list:
            print('Условия:')
            for key in self.conditions_list:
                print('-', key)
        else:
            print('Условий не найдено!')
        print('----------------------------------------------')


class SearchQuery:
    '''Класс поискового запроса'''
    def __init__(self, search_text):
        self.vacancy_list = []
        self.search_text = search_text.strip()
        self.page_number = 0
        self.cur_vac_num = 0
        self.sum_vac = 0
        self.search_time = 0

    def current_vacancy_number(self, value):
        self.cur_vac_num = value

    def current_vacancy_number_return(self):
        return self.cur_vac_num

    def sum_vacancies(self, value):
        self.sum_vac = value

    def sum_vacancies_return(self):
        return self.sum_vac

    def start_search(self):
        self.search_time_start = time.time()
        search_url = URL + "/search/vacancy?clusters=true&area=2&" + \
            "enable_snippets=true&text={0}".format(
                urllib.parse.quote_plus(self.search_text))
        count_pages = self.count_pages(search_url)
        if count_pages is None:
            print('Записей не найдено!')
        else:
            for i in range(0, count_pages):
                search_url = URL + "/search/vacancy?clusters=true&area=2" + \
                    "&enable_snippets=true&text={0}&page={1}".format(
                        urllib.parse.quote_plus(self.search_text), str(i))
                self.search_on_page(search_url)

    def search_on_page(self, search_url):
        page = get_html(search_url)
        soup = BeautifulSoup(page, 'lxml')
        vacancy = soup.find(
            'div', class_="search-result").find_all('div', class_="search-result-item__head")
        for key in vacancy:
            temp = key.find('a')
            temp1 = temp.get('href').split('?')
            vacancy_url = temp1[0]
            new_vacancy = Vacancy(vacancy_url)
            self.vacancy_list.append(new_vacancy)

    def count_pages(self, search_url):
        try:
            page = get_html(search_url)
            soup = BeautifulSoup(page, 'lxml')
            search_result = soup.find(
                'div', class_='resumesearch__result-count').get_text()
            print(search_result)
        except:
            return
        temp = ''
        for i in search_result:
            if i in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                temp = temp + i
        if 0 < int(temp) < 20:
            sum_pages = 1
        else:
            sum_pages = int(int(temp) // 20)
        if sum_pages != None:
            self.sum_vacancies(int(temp))
            return sum_pages
        else:
            return 0
    
    def get_vacancy_information(self, requirments, conditions, expectations):
        i = 1
        for key in self.vacancy_list:
            self.current_vacancy_number(i)
            key.search_on_page()
            key.description_parse(requirments, conditions, expectations)
            self.progress_bar()
            #print('Вакансия: ', i)
            #key.print_result()
            i += 1
    
    def progress_bar(self):
        prog = int((self.cur_vac_num / self.sum_vac)*100)
        print('Обработка данных выполнена на {0}%\r'.format(prog), end='')

    def format_string(self, string):
        temp = string.split("'")
        temp2 = ''
        for key in temp:
            temp2 += key
        return temp2
    
    def db_add_qustion(self):
        while True:
            q_text = input('Хотите добавить в базу данных?(y/n): ')
            if q_text == 'y':
                return 1
            elif q_text == 'n':
                return 0
            else:
                'Неправильный ввод!'

    def insert_into_db(self, server_name, db_name):
        if self.vacancy_list:
            ans = self.db_add_qustion()
            if ans == 1:
                start = time.time()
                i = 0
                conn = hh_mssql.MSSQLConnection(server_name, db_name)
                print('\nДобавление в БД...')
                id_vacancy = 0
                id_query = conn.insert_query(self.search_text, self.search_time)
                for key in self.vacancy_list:
                    try:    
                        id_vacancy = conn.insert_vacancy(key.vacancy_name, key.vacancy_company, key.vacancy_salary, 
                        key.currency, key.vacancy_city, key.vacancy_metro, key.vacancy_experience,
                        key.vacancy_date, key.vacancy_url)
                        for c_key in key.conditions_list:
                            id_con = conn.insert_text_condition(self.format_string(c_key))
                            conn.insert_vac_con(id_vacancy, id_con)
                        for e_key in key.expectations_list:
                            id_exp = conn.insert_text_expectation(self.format_string(e_key))
                            conn.insert_vac_exp(id_vacancy, id_exp)
                        for r_key in key.requirments_list:
                            id_req = conn.insert_text_requerments(self.format_string(r_key))
                            conn.insert_vac_req(id_vacancy, id_req)
                        conn.insert_query_vacancy(id_vacancy, id_query)
                    except:
                        conn.delete_after_error(id_vacancy)
                    i += 1
                finish = time.time() - start
                print('\nДобавление вакансий в базу длилось ', finish, ' секунд.')
            elif ans == 0:
                print('\nОперация добавления отменена!')
            else:
                print('Ошибка!')

    def end_of_search(self):
        if self.vacancy_list:
            self.search_time = time.time() - self.search_time_start
            print('Поиск и обработка вакансий длились ', self.search_time, ' секунд.')