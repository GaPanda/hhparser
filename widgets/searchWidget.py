from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QStatusBar,
                             QMenuBar, QDesktopWidget, QApplication, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QProgressBar)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QRect
from PyQt5.QtGui import QIcon, QFont
from libs.hh_parse import SearchQuery
from libs.hh_config import Data

class SearchWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        #Labels
        self.search_text = QLabel('Поисковый запрос: ', self)
        self.search_text.setGeometry(QRect(30, 40, 131, 16))
        self.time_label_name = QLabel('Время обработки: ', self)
        self.time_label_name.setGeometry(QRect(30, 100, 131, 16))
        self.time_label = QLabel('0 секунд', self)
        self.time_label.setGeometry(QRect(190, 100, 47, 16))
        self.vacancy_count = QLabel('Найденные вакансий: ', self)
        self.vacancy_count.setGeometry(QRect(30, 130, 131, 16))
        self.vacancy_count_number = QLabel('0', self)
        self.vacancy_count_number.setGeometry(QRect(190, 130, 47, 16))
        self.vacancy_analized = QLabel('Обработанные вакансий: ', self)
        self.vacancy_analized.setGeometry(QRect(30, 160, 131, 16))
        self.vacancy_analized_number = QLabel('0', self)
        self.vacancy_analized_number.setGeometry(QRect(190, 160, 47, 16))
        self.progress_text = QLabel('Прогресс: ', self)
        self.progress_text.setGeometry(QRect(30, 70, 131, 21))
        self.name = QLabel('Поиск вакансий по текстовому запросу', self)
        self.name.setGeometry(QRect(10, 10, 241, 16))
        font = QFont()
        font.setPointSize(10)
        self.name.setFont(font)
        #LineEdits
        self.search_text_edit = QLineEdit(self)
        self.search_text_edit.setGeometry(QRect(190, 40, 271, 21))
        #Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(QRect(190, 70, 271, 23))
        self.progress_bar.setProperty("value", 0)
        #Buttons
        self.search_button = QPushButton('Поиск', self)
        self.search_button.setGeometry(QRect(310, 180, 75, 23))
        self.cancel_button = QPushButton('Отмена', self)
        self.cancel_button.setGeometry(QRect(390, 180, 75, 23))
        self.search_button.clicked.connect(self.search_button_click)
        self.cancel_button.clicked.connect(self.cancel_button_click)

    def search_button_click(self):
        text = str(self.search_text_edit.text())
        self.cancel_button.setEnabled(1)
        self.search_button.setEnabled(0)
        #self.start_query_search(text)

    def cancel_button_click(self):
        self.cancel_button.setEnabled(0)
        self.search_button.setEnabled(1)
        
    def start_query_search(self, text):
        try:
            self.data = Data()
            self.data.load_from_conf()
            print(text)
            print(self.data.rtimeout())
            self.searchQuery = SearchQuery(text, self.data.rtimeout())
            self.searchQuery.start_search()
            self.searchQuery.get_vacancy_information(self.data.rrequirments(), self.data.rconditions(), self.data.rexpectations())
        except:
            pass