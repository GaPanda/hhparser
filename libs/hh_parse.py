# -*- coding: utf-8 -*-

import re
from urllib.request import urlopen
from urllib import parse
import time
from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

URL = "https://hh.ru"

class Vacancy:
    '''Класс описывающий вакансию'''
    def __init__(self, url, timeout):
        self.timeout = timeout
        self.vacancy_url = url
        self.requirments_list = []
        self.conditions_list = []
        self.expectations_list = []

    def get_html(self, url, timeout):
        '''Получение кода страницы'''
        #Timeout при запросе
        time.sleep(timeout)
        page = urlopen(url)
        return page.read()

    def search_on_page(self):
        '''Поиск данных на странице вакансии'''
        page = self.get_html(self.vacancy_url, self.timeout)
        soup = BeautifulSoup(page, 'lxml')
        self.vacancy_name = soup.find(
            'h1', class_="title b-vacancy-title").get_text().strip()
        self.vacancy_company = soup.find(
            'div', class_="companyname").get_text().strip()
        self.vacancy_salary = soup.find('td', class_="l-content-colum-1 b-v-info-content").find(
            'div', class_="l-paddings").get_text().strip()
        try:
            self.vacancy_salary = soup.find('td', class_="l-content-colum-1 b-v-info-content").find(
            'meta', itemprop = "baseSalary").get('content').strip()
            self.currency = soup.find('td', class_="l-content-colum-1 b-v-info-content").find(
            'meta', itemprop = "salaryCurrency").get('content').strip()
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

class StringCalc:
    def __init__(self, string):
        self.operators = {'&': (1, lambda a, b: a.intersection(b)),
                         '+': (2, lambda a, b: a.union(b)),
                         '/': (2, lambda a, b: a.difference(b))}
        self.search_string = string

    def add_variables(self, var):
        self.variables = var

    def dictionary(self, dicti):
        self.dictionary = dicti

    def get_variables(self):
        queries = re.findall(r'([\'\"](\w*|\W)*[\'\"])', self.search_string)
        temp_list = []
        for key in set(queries):
            node = NodeQuery(key[0])
            temp_list.append(node)
        return temp_list
    
    def return_set_for_calc(self, query_number):
        for key in self.dictionary:
            x = key.return_query_number()
            if x == query_number:
                return key.return_vacancies()

    def replace_query_name(self):
        for key in self.dictionary:
            self.search_string = self.search_string.replace(key.return_name_query(),
                                 ('"' + str(key.return_query_number()) + '"'))

    def parse(self, formula_string):
        number = ''
        for s in formula_string:
            if s in '1234567890"': # если символ - цифра, то собираем число
                number += s
            elif number: # если символ не цифра, то выдаём собранное число и начинаем собирать заново
                yield number
                number = ''
            if s in self.operators or s in "()": # если символ - оператор или скобка, то выдаём как есть
                yield s 
        if number:  # если в конце строки есть число, выдаём его
            yield number

    def shunting_yard(self, parsed_formula):
        stack = []  # в качестве стэка используем список
        for token in parsed_formula:
            # если элемент - оператор, то отправляем дальше все операторы из стека, 
            # чей приоритет больше или равен пришедшему,
            # до открывающей скобки или опустошения стека.
            # здесь мы пользуемся тем, что все операторы право-ассоциативны
            if token in self.operators: 
                while stack and stack[-1] != "(" and self.operators[token][0] <= self.operators[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                # если элемент - закрывающая скобка, выдаём все элементы из стека, до открывающей скобки,
                # а открывающую скобку выкидываем из стека.
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                # если элемент - открывающая скобка, просто положим её в стек
                stack.append(token)
            else:
                # если элемент - число, отправим его сразу на выход
                yield token
        while stack:
            yield stack.pop()

    def calc(self, polish):
        stack = []

        for token in polish:
            if token in self.operators:  # если приходящий элемент - оператор,
                y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                stack.append(self.operators[token][1](x, y)) # вычисляем оператор, возвращаем в стек
            else:
                stack.append(self.return_set_for_calc(int(token.strip('"'))))
        if len(stack) == 1:
            return stack[0] # результат вычисления - единственный элемент в стеке
        else:
            return 0

class NodeQuery:
    def __init__(self, name):
        self.name_query = name

    def set_query_number(self, num):
        self.query_number = num

    def set_vacancies(self, vac):
        self.vacancies = vac

    def return_name_query(self):
        return self.name_query

    def return_query_number(self):
        return self.query_number

    def return_vacancies(self):
        return self.vacancies

class SearchQuery(QObject):
    
    vacancy_count_signal = pyqtSignal(int)
    vacancy_analized_signal = pyqtSignal(int)
    query_finished_signal = pyqtSignal()

    '''Класс поискового запроса'''
    def set_query_config(self, search_text, timeout, requirments, expectations, conditions):
        self.vacancy_list = []       
        self.vacancy_analized = 0
        self.vacancy_count = 0
        self.search_time = 0
        self.search_text = search_text.strip()
        self.timeout = timeout
        self.requirments = requirments
        self.expectations = expectations
        self.conditions = conditions

    @pyqtSlot()
    def set_vacancy_count(self, value):
        self.vacancy_count = value
        self.vacancy_count_signal.emit(self.vacancy_count)

    @pyqtSlot()
    def set_vacancy_analized(self, value):
        self.vacancy_analized = value
        self.vacancy_analized_signal.emit(self.vacancy_analized)

    def set_search_time(self, time):
        self.search_time = time

    def get_html(self, url, timeout):
        '''Получение кода страницы'''
        #Timeout при запросе
        time.sleep(timeout)
        page = urlopen(url)
        return page.read()

    def start_search(self):
        if len(self.search_text) > 200:
            raise Exception('Запрос больше 200 символов.')
        calc = StringCalc(self.search_text)
        dictionary = calc.get_variables()
        if dictionary:
            i = 0
            for node in dictionary:
                node.set_vacancies(set(self.query_search(node.return_name_query())))
                node.set_query_number(i)
                i += 1
            calc.dictionary(dictionary)
            calc.replace_query_name()
            vacancy = calc.calc(calc.shunting_yard(calc.parse(calc.search_string)))
            if vacancy:
                for key in vacancy:
                    self.vacancy_list.append(Vacancy(key, self.timeout))
                self.set_vacancy_count(len(self.vacancy_list))
            elif vacancy == 0:
                raise Exception('Возможно вы допустили ошибку в составлении запроса.')
            else:
                raise Exception('Вакансий по данному запросу не найдено.')
        else:
            raise Exception('Неправильно составлен запрос.')

    def query_search(self, search_text):
        vacancy_list = []
        self.search_time_start = time.time()
        search_url = URL + "/search/vacancy?clusters=true&area=2&" + \
            "enable_snippets=true&text={0}".format(
                parse.quote_plus(search_text))
        count_pages = self.count_pages(search_url)
        if count_pages:
            for i in range(0, count_pages):
                search_url = URL + "/search/vacancy?clusters=true&area=2" + \
                    "&enable_snippets=true&text={0}&page={1}".format(
                        parse.quote_plus(search_text), str(i))
                self.search_on_page(search_url, vacancy_list)
        return vacancy_list

    def search_on_page(self, search_url, vacancy_list):
        page = self.get_html(search_url, self.timeout)
        soup = BeautifulSoup(page, 'lxml')
        vacancy = soup.find(
            'div', class_="search-result").find_all('div', class_="search-result-item__head")
        for key in vacancy:
            temp = key.find('a')
            temp1 = temp.get('href').split('?')
            vacancy_url = temp1[0]
            vacancy_list.append(vacancy_url)

    def count_pages(self, search_url):
        try:
            page = self.get_html(search_url, self.timeout)
            soup = BeautifulSoup(page, 'lxml')
            search_result = soup.find(
                'div', class_='resumesearch__result-count').get_text()
        except:
            return
        temp = ''
        for i in search_result:
            if i in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                temp = temp + i
        if 0 < int(temp) < 20:
            sum_pages = 1
        else:
            sum_pages = int(int(temp) // 20) + 1
        if sum_pages != None:
            if sum_pages < 100:
                return sum_pages
            else:
                raise Exception('В подзапросе больше 2000 вакансий.')
        else:
            return 0

    def get_vacancy_information(self, start_time):
        i = 1
        for key in self.vacancy_list:
            self.set_vacancy_analized(i)
            key.search_on_page()
            key.description_parse(self.requirments, self.conditions, self.expectations)
            print('Вакансия: ', i)
            key.print_result()
            i += 1
        self.search_time = int(time.time() - start_time)
        self.query_finished_signal.emit()