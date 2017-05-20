from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QStatusBar,
                             QMenuBar, QDesktopWidget, QApplication, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QProgressBar)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QRect
from PyQt5.QtGui import QIcon, QFont
from libs.hh_parse import SearchQuery
from libs.hh_config import Data

class SearchFileWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        #Labels
        self.search_file = QLabel('Файл с запросами: ', self)
        self.search_file.setGeometry(QRect(30, 40, 131, 16))
        self.progress_text = QLabel('Прогресс: ', self)
        self.progress_text.setGeometry(QRect(30, 70, 131, 21))
        self.time_label_name = QLabel('Время обработки: ', self)
        self.time_label_name.setGeometry(QRect(30, 160, 131, 16))
        self.time_label = QLabel('0 сек', self)
        self.time_label.setGeometry(QRect(190, 160, 281, 16))
        self.vacancy_count = QLabel('Найденные вакансий: ', self)
        self.vacancy_count.setGeometry(QRect(30, 190, 131, 16))
        self.vacancy_count_number = QLabel('0', self)
        self.vacancy_count_number.setGeometry(QRect(190, 190, 131, 16))
        self.vacancy_analized = QLabel('Обработанные вакансий: ', self)
        self.vacancy_analized.setGeometry(QRect(30, 220, 131, 16))
        self.vacancy_analized_number = QLabel('0', self)
        self.vacancy_analized_number.setGeometry(QRect(190, 220, 131, 16))
        self.number_query = QLabel('Запрос №: ', self)
        self.number_query.setGeometry(QRect(30, 100, 131, 16))
        self.number_query_value = QLabel('0', self)
        self.number_query_value.setGeometry(QRect(190, 100, 131, 16))
        self.query_text = QLabel('Текст запроса: ', self)
        self.query_text.setGeometry(QRect(30, 130, 131, 16))
        self.query_text_value = QLabel("", self)
        self.query_text_value.setGeometry(QRect(190, 130, 281, 16))
        self.name = QLabel('Поиск вакансий с загрузкой запросов из файла', self)
        self.name.setGeometry(QRect(10, 10, 241, 16))
        font = QFont()
        font.setPointSize(10)
        self.name.setFont(font)
        #LineEdits
        self.search_file_edit = QLineEdit(self)
        self.search_file_edit.setGeometry(QRect(190, 40, 191, 21))
        #Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(QRect(190, 70, 271, 23))
        self.progress_bar.setProperty("value", 0)
        #Buttons
        self.search_button = QPushButton('Поиск', self)
        self.search_button.setGeometry(QRect(310, 250, 75, 23))
        self.search_button.clicked.connect(self.search_button_clicked)
        self.cancel_button = QPushButton('Отмена', self)
        self.cancel_button.setGeometry(QRect(390, 250, 75, 23))
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.file_open_button = QPushButton('Открыть', self)
        self.file_open_button.setGeometry(QRect(390, 40, 71, 21))
        self.file_open_button.clicked.connect(self.file_open_button_clicked)

    def search_button_clicked(self):
        text = str(self.search_text_edit.text)
        self.start_query_search(text)
        self.search_button.setEnabled(0)

    def cancel_button_clicked(self):
        pass
        
    def file_open_button_clicked(self):
        pass