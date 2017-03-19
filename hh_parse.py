import urllib.request
import urllib.parse
import re
import sys
from bs4 import BeautifulSoup
import hh_mssql

URL = "https://spb.hh.ru"


def get_html(url):
    '''Получение кода страницы'''
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
            self.vacancy_salary = "Отсутствует"
            self.currency = "Отсутствует" 
        try:
            self.vacancy_date = soup.find('time', class_="vacancy-sidebar__publication-date").get('datetime')[:10]
        except:
            self.vacancy_date = "Отсутствует"

        self.vacancy_city = soup.find('td', class_="l-content-colum-2 b-v-info-content").find(
            'div', class_="l-paddings").get_text()
        self.vacancy_experience = soup.find('td', class_="l-content-colum-3 b-v-info-content").find(
            'div', class_="l-paddings").get_text()
        self.vacancy_description = soup.find(
            'div', class_="b-vacancy-desc-wrapper")

    def description_parse(self):
        requirments = ['Требования:', 'Требования к кандидату:',
                       'Требования', 'Требования к кандидату', 'Что для нас важно:']
        conditions = ['Условия:', 'Условия', 'Условия, которые мы предлагаем:',
                      'Условия, которые мы предлагаем', 'От нас:', 'От нас',
                      'Мы предлагаем:', 'Мы предлагаем']
        expectations = ['Ожидания:', 'Обязанности:',
                        'Задачи:', 'Ожидания', 'Обязанности', 'Задачи',
                        'Основные задачи', 'Основные задачи:',
                        'Ваши ежедневные задачи', 'Ваши ежедневные задачи:',
                        'Ключевые задачи:', 'Ключевые задачи', 'Задачи для тебя:',
                        'Основными задачами для Вас станет:']
        tag_text = self.vacancy_description.find_all(['strong', 'ul'])
        i = 0
        for key in tag_text:
            # print(key.get_text())
            if key.get_text().strip() in requirments:
                self.requirments_list = self.tag_text_analyze(tag_text, i + 1)
                i += 1
            elif key.get_text().strip()  in conditions:
                self.conditions_list = self.tag_text_analyze(tag_text, i + 1)
                i += 1
            elif key.get_text().strip()  in expectations:
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
              '\nДата публикации: ', self.vacancy_date,
              '\nИмя компании: ', self.vacancy_company,
              '\nЗарплата: ', self.vacancy_salary,
              '\nГород: ', self.vacancy_city,
              '\nURL: ', self.vacancy_url)
        print('Требования:')
        for key in self.requirments_list:
            print('-', key)
        print('Ожидания:')
        for key in self.expectations_list:
            print('-', key)
        print('Условия:')
        for key in self.conditions_list:
            print('-', key)


class SearchQuery:
    '''Класс поискового запроса'''

    def __init__(self, search_text):
        self.vacancy_list = []
        self.search_text = search_text.strip()
        self.page_number = 0
        self.cur_vac_num = 0
        self.sum_vac = 0

    def current_vacancy_number(self, value):
        self.cur_vac_num = value

    def current_vacancy_number_return(self):
        return self.cur_vac_num

    def sum_vacancies(self, value):
        self.sum_vac = value

    def sum_vacancies_return(self):
        return self.sum_vac

    def start_search(self):
        search_url = URL + "/search/vacancy?clusters=true&area=2&" + \
            "enable_snippets=true&text={0}".format(
                urllib.parse.quote_plus(self.search_text))
        count_pages = self.count_pages(search_url)
        print(count_pages)
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
            return sum_pages
        else:
            return 0

    def full_vacancy_information(self):
        i = 1
        for key in self.vacancy_list:
            key.search_on_page()
            key.description_parse()
            print('Вакансия: ', i)
            key.print_result()
            i += 1

    def insert_into_db(self, server_name, db_name):
        conn = MSSQLConnection(server_name, db_name)
        conn.insert_name_query(self.search_text)

    def exit(self):
        sys.exit(0)


def main():
    server_name = 'DESKTOP\SQLEXPRESS'
    db_name = 'hh'
    search_text = input('Поисковый запрос: ')
    my_query = SearchQuery(search_text)
    my_query.start_search()
    my_query.full_vacancy_information()

if __name__ == '__main__':
    main()
