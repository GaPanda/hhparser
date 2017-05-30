# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QStatusBar,
                             QMenuBar, QDesktopWidget, QApplication, QStackedWidget, QHBoxLayout)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QRect, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

from widgets.searchWidget import SearchWidget
from widgets.searchFileWidget import SearchFileWidget
from widgets.serverSettingsWidget import ServerSettingsWidget
from widgets.searchSettingsWidget import SearchSettingsWidget
from widgets.queryWidget import QueryWidget
from widgets.infoWidget import InfoWidget
from widgets.vacancyWidget import VacancyWidget

class MainWindow(QMainWindow):
    sig_status_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.initForm()

    def initForm(self):
        #Query
        self.status = False
        #Search Action
        self.search_action = QAction('&Поиск вакансий из запроса', self)
        self.search_action.triggered.connect(self.set_main_search_widget)
        self.search_file_action = QAction('&Поиск вакансий из файла', self)
        self.search_file_action.triggered.connect(self.set_main_search_file_widget)
        self.show_query = QAction('&Просмотр запросов', self)
        self.show_query.triggered.connect(self.set_main_query_widget)
        self.settings_search_action = QAction('&Настройка параметров поиска', self)
        self.settings_search_action.triggered.connect(self.set_main_search_settings_widget)
        self.settings_database_action = QAction('&Настройка БД', self)
        self.settings_database_action.triggered.connect(self.set_main_server_settings_widget)
        self.about_action = QAction('&О программе', self)
        self.about_action.triggered.connect(self.set_main_info_widget)
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
        self.status_bar.showMessage('Готов!')
        #Windows settings
        self.setMinimumSize(500, 400)   
        self.resize(500, 400)
        self.center()
        self.setWindowIcon(QIcon())
        self.setWindowTitle('Программа для парсинга вакансий')
        self.show()
        self.stack_widget()

    def stack_widget(self):
        self.Stack = QStackedWidget(self)

        self.searchWidget = SearchWidget(self.status_bar, self.status)
        self.searchFileWidget = SearchFileWidget(self.status_bar, self.status)
        self.serverSettingsWidget = ServerSettingsWidget(self.status)
        self.searchSettingsWidget = SearchSettingsWidget(self.status)
        self.queryWidget = QueryWidget()
        self.infoWidget = InfoWidget()

        self.searchWidget.sig_work.connect(self.set_status)
        self.searchFileWidget.sig_work.connect(self.set_status)
        self.sig_status_changed.connect(self.searchWidget.status_changed)
        self.sig_status_changed.connect(self.searchFileWidget.status_changed)
        self.sig_status_changed.connect(self.searchSettingsWidget.status_changed)
        self.sig_status_changed.connect(self.serverSettingsWidget.status_changed)

        self.Stack.addWidget(self.searchWidget)
        self.Stack.addWidget(self.searchFileWidget)
        self.Stack.addWidget(self.serverSettingsWidget)
        self.Stack.addWidget(self.searchSettingsWidget)
        self.Stack.addWidget(self.queryWidget)
        self.Stack.addWidget(self.infoWidget)

        self.setCentralWidget(self.Stack)

    @pyqtSlot(bool)
    def set_status(self, status: bool):
        self.status = status
        self.sig_status_changed.emit(self.status)

    def set_main_search_widget(self):
        self.Stack.setCurrentIndex(0)
        self.resize(500, 400)

    def set_main_search_file_widget(self):
        self.Stack.setCurrentIndex(1)
        self.resize(500, 400)

    def set_main_server_settings_widget(self):
        self.Stack.setCurrentIndex(2)
        self.resize(500, 400)

    def set_main_search_settings_widget(self):
        self.Stack.setCurrentIndex(3)
        self.resize(500, 400)

    def set_main_query_widget(self):
        self.Stack.setCurrentIndex(4)
        self.resize(600, 400)

    def set_main_info_widget(self):
        self.Stack.setCurrentIndex(5)
        self.resize(500, 400)


    def center(self):
        fr_geo = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        fr_geo.moveCenter(center)
        self.move(fr_geo.topLeft())