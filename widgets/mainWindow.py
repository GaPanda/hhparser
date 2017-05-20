# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QStatusBar,
                             QMenuBar, QDesktopWidget, QApplication, QStackedWidget, QHBoxLayout)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QRect
from PyQt5.QtGui import QIcon, QFont
from widgets.searchWidget import SearchWidget
from widgets.searchFileWidget import SearchFileWidget
from widgets.serverSettingsWidget import ServerSettingsWidget
from widgets.searchSettingsWidget import SearchSettingsWidget

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initForm()

    def initForm(self):
        #Search Action
        self.search_action = QAction('&Поиск вакансий из запроса', self)
        self.search_action.triggered.connect(self.set_main_search_widget)
        self.search_file_action = QAction('&Поиск вакансий из файла', self)
        self.search_file_action.triggered.connect(self.set_main_search_file_widget)
        self.show_query = QAction('&Просмотр запросов', self)
        self.settings_search_action = QAction('&Настройка параметров поиска', self)
        self.settings_search_action.triggered.connect(self.set_main_search_settings_widget)
        self.settings_database_action = QAction('&Настройка БД', self)
        self.settings_database_action.triggered.connect(self.set_main_server_settings_widget)
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
        self.setMaximumSize(500,400)
        self.setMinimumSize(500,400)
        self.center()
        self.setWindowIcon(QIcon())
        self.setWindowTitle('Программа для парсинга вакансий')
        self.show()
        self.stack_widget()

    def stack_widget(self):
        self.Stack = QStackedWidget(self)

        self.searchWidget = SearchWidget()
        self.searchFileWidget = SearchFileWidget()
        self.serverSettingsWidget = ServerSettingsWidget()
        self.searchSettingsWidget = SearchSettingsWidget()

        self.Stack.addWidget(self.searchWidget)
        self.Stack.addWidget(self.searchFileWidget)
        self.Stack.addWidget(self.serverSettingsWidget)
        self.Stack.addWidget(self.searchSettingsWidget)

        self.setCentralWidget(self.Stack)

    def set_main_search_widget(self):
        self.Stack.setCurrentIndex(0)

    def set_main_search_file_widget(self):
        self.Stack.setCurrentIndex(1)

    def set_main_server_settings_widget(self):
        self.Stack.setCurrentIndex(2)

    def set_main_search_settings_widget(self):
        self.Stack.setCurrentIndex(3)
    

    def center(self):
        fr_geo = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        fr_geo.moveCenter(center)
        self.move(fr_geo.topLeft())