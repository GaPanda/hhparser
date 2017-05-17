# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QStatusBar,
                             QMenuBar, QDesktopWidget, QApplication, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QProgressBar)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QRect
from PyQt5.QtGui import QIcon, QFont

class SearchWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        #Labels
        self.search_text = QLabel('Поисковый запрос: ', self)
        self.search_text.setGeometry(QRect(10, 10, 101, 16))
        self.time_label_name = QLabel('Время обработки: ', self)
        self.time_label_name.setGeometry(QRect(10, 70, 101, 16))
        self.time_label = QLabel('0 секунд', self)
        self.time_label.setGeometry(QRect(210, 70, 47, 13))
        self.vacancy_count = QLabel('Количество найденных вакансий: ', self)
        self.vacancy_count.setGeometry(QRect(10, 100, 181, 16))
        self.vacancy_count_number = QLabel('0', self)
        self.vacancy_count_number.setGeometry(QRect(210, 100, 47, 13))
        self.vacancy_analized = QLabel('Количество обработанных вакансий: ', self)
        self.vacancy_analized.setGeometry(QRect(10, 130, 191, 16))
        self.vacancy_analized_number = QLabel('0', self)
        self.vacancy_analized_number.setGeometry(QRect(210, 130, 47, 13))
        self.progress_text = QLabel('Прогресс: ', self)
        self.progress_text.setGeometry(QRect(10, 40, 91, 21))
        #LineEdits
        self.search_text_edit = QLineEdit(self)
        self.search_text_edit.setGeometry(QRect(210, 10, 191, 21))
        #Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(QRect(210, 40, 281, 23))
        self.progress_bar.setProperty("value", 0)
        #Buttons
        self.search_button = QPushButton('Поиск', self)
        self.search_button.setGeometry(QRect(410, 10, 75, 21))
        self.cancel_button = QPushButton('Отмена', self)
        self.cancel_button.setGeometry(QRect(410, 150, 75, 23))
        self.show()

class ServerSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        #Buttons
        self.save_button = QPushButton('Сохранить', self)
        self.save_button.setGeometry(QRect(224, 160, 81, 23))
        self.cancel_button = QPushButton('Отменить', self)
        self.cancel_button.setGeometry(QRect(310, 160, 81, 23))
        self.test_button = QPushButton('Проверка соединения', self)
        self.test_button.setGeometry(QRect(100, 160, 121, 23))
        #Labels
        self.label = QLabel('Настройка сервера и базы данных:', self)
        self.label.setGeometry(QRect(30, 10, 221, 16))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.server_name = QLabel('Имя сервера: ', self)
        self.server_name.setGeometry(QRect(100, 40, 101, 21))
        self.database_name = QLabel('Имя базы данных: ', self)
        self.database_name.setGeometry(QRect(100, 130, 101, 21))
        self.user_name = QLabel('Пользователь: ', self)
        self.user_name.setGeometry(QRect(100, 70, 101, 21))
        self.user_password = QLabel('Пароль: ', self)
        self.user_password.setGeometry(QRect(100, 100, 101, 21))
        #LineEdits
        self.server_name_edit = QLineEdit(self)
        self.server_name_edit.setGeometry(QRect(210, 40, 181, 21))
        self.database_name_edit = QLineEdit(self)
        self.database_name_edit.setGeometry(QRect(210, 70, 181, 21))
        self.user_name_edit = QLineEdit(self)
        self.user_name_edit.setGeometry(QRect(210, 100, 181, 21))
        self.user_password_edit = QLineEdit(self)
        self.user_password_edit.setGeometry(QRect(210, 130, 181, 21))
        self.show()

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initForm()

    def initForm(self):
        #Search Action
        self.search_action = QAction('&Поиск вакансий из запроса', self)
        self.search_file_action = QAction('&Поиск вакансий из файла', self)
        self.show_query = QAction('&Просмотр запросов', self)
        self.settings_search_action = QAction('&Настройка БД', self)
        self.settings_database_action = QAction('&Настройка параметров поиска', self)
        self.about_action = QAction('&О программе', self)
        #Menu Bar
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu('&Поиск')
        self.file_menu.addAction(self.search_action)
        self.file_menu.addAction(self.search_file_action)
        self.file_menu_2 = self.menu_bar.addMenu('&Просмотр')
        self.file_menu_2.addAction(self.show_query)
        self.file_menu_3 = self.menu_bar.addMenu('&Настройки')
        self.file_menu_3.addAction(self.settings_database_action)
        self.file_menu_3.addAction(self.settings_search_action)
        self.file_menu_4 = self.menu_bar.addMenu('&Справка')
        self.file_menu_4.addAction(self.about_action)
        #Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready!')

        #Windows settings
        searchWidget = SearchWidget()
        self.setCentralWidget(searchWidget)
        self.setMaximumSize(500,400)
        self.setMinimumSize(500,400)
        self.center()
        self.setWindowIcon(QIcon())
        self.setWindowTitle('Программа для парсинга вакансий')
        self.show()

    def center(self):
        fr_geo = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        fr_geo.moveCenter(center)
        self.move(fr_geo.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainWindow()
    sys.exit(app.exec_())