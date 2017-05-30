from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QMessageBox,
                             QDesktopWidget, QApplication, QLabel, QTableView, QAbstractItemView)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QRect, QDateTime, QItemSelectionModel
from PyQt5.QtGui import QIcon, QFont, QStandardItemModel, QStandardItem
from libs.hh_config import Data
from libs.hh_mssql import MssqlConnection
from widgets.vacancyWidget import VacancyWidget

class QueryWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initWidget()
    
    def initWidget(self):
        self.name = QLabel("Просмотр запросов в базе данных", self)
        self.name.setGeometry(QRect(10, 10, 241, 16))
        font = QFont()
        font.setPointSize(10)
        self.name.setFont(font)
        self.tableView = QTableView(self)
        self.tableView.setGeometry(QRect(30, 60, 545, 291))
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.refresh_button = QPushButton("Обновить таблицу", self)
        self.refresh_button.setGeometry(QRect(30, 30, 111, 23))
        self.refresh_button.clicked.connect(self.load_data)
        self.show_all_vacancies_button = QPushButton("Посмотреть вакансии", self)
        self.show_all_vacancies_button.setGeometry(150, 30, 131, 23)
        self.show_all_vacancies_button.clicked.connect(self.load_vacancies)

    def load_data(self):
        model = QStandardItemModel()
        model.setColumnCount(5)
        headerNames = []
        headerNames.append("ID")
        headerNames.append("Имя")
        headerNames.append("Дата")
        headerNames.append("Время обработки")
        headerNames.append("Кол-во вакансий")
        model.setHorizontalHeaderLabels(headerNames)
        self.config = Data()
        self.config.load_from_conf()
        self.conn = MssqlConnection(self.config.rserver_name(), self.config.rdb_name(), self.config.rusername(), self.config.rpassword())
        try:
            query_list = self.conn.queries_show()
            for row in query_list:
                row_data = []
                i = 0
                for key in row:
                    if i == 2:
                        qd = QDateTime(key)
                        item = QStandardItem(qd.toString("dd.MM.yyyy hh:mm"))
                        item.setEditable(False)
                    else:
                        item = QStandardItem(str(key))
                        item.setEditable(False)
                    row_data.append(item)
                    i += 1
                model.appendRow(row_data)
            self.tableView.setModel(model)
            self.tableView.setColumnWidth(0, 40)
            self.tableView.setColumnWidth(1, 125)
            self.tableView.setColumnWidth(2, 105)
            self.tableView.setColumnWidth(3, 115)
            self.tableView.setColumnWidth(4, 115)
        except:
            QMessageBox.warning(self, 'Ошибка!', 'Ошибка при загрузке таблицы!', QMessageBox.Ok)
    
    def load_vacancies(self):
        try:
            index = self.tableView.selectedIndexes()
            self.widget = VacancyWidget(index[0].data(), self.conn)
            self.widget.show()
        except:
           QMessageBox.warning(self, 'Ошибка!', 'Выберите строку с запросом!', QMessageBox.Ok)
        