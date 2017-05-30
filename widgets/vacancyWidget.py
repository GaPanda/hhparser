from PyQt5 import QtCore, QtGui, QtWidgets

class VacancyWidget(QtWidgets.QWidget):
    def __init__(self, index, conn):
        super().__init__()
        self.index = index
        self.conn = conn
        self.initWidget()        

    def initWidget(self):
        self.label = QtWidgets.QLabel('Список вакансий:', self)
        self.label.setGeometry(QtCore.QRect(20, 10, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setGeometry(QtCore.QRect(20, 60, 421, 321))
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(460, 160, 341, 221))
        self.tab = QtWidgets.QWidget()
        self.tableView_2 = QtWidgets.QTableView(self.tab)
        self.tableView_2.setGeometry(QtCore.QRect(0, 0, 330, 195))
        self.tabWidget.addTab(self.tab, "Требования")

        self.tab_2 = QtWidgets.QWidget()
        self.tableView_3 = QtWidgets.QTableView(self.tab_2)
        self.tableView_3.setGeometry(QtCore.QRect(0, 0, 330, 195))
        self.tabWidget.addTab(self.tab_2, "Ожидания")

        self.tab_3 = QtWidgets.QWidget()
        self.tableView_4 = QtWidgets.QTableView(self.tab_3)
        self.tableView_4.setGeometry(QtCore.QRect(0, 0, 330, 195))
        self.tabWidget.addTab(self.tab_3, "Условия")

        self.pushButton = QtWidgets.QPushButton("Посмотреть полную информацию", self)
        self.pushButton.setGeometry(QtCore.QRect(20, 30, 191, 23))
        self.pushButton.clicked.connect(self.show_all_info)

        self.pushButton_2 = QtWidgets.QPushButton("Отмена", self)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 30, 75, 23))
        self.pushButton_2.clicked.connect(self.undo_all_info)

        self.label_2 = QtWidgets.QLabel("Информация о вакансии", self)
        self.label_2.setGeometry(QtCore.QRect(460, 10, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)

        self.pushButton_3 = QtWidgets.QPushButton("Открыть в браузере", self)
        self.pushButton_3.setGeometry(QtCore.QRect(660, 130, 130, 23))
        self.pushButton_3.clicked.connect(self.open_browser)

        self.name_vacancy = QtWidgets.QLabel("NULL", self)
        self.name_vacancy.setGeometry(QtCore.QRect(470, 30, 400, 13))

        self.name_company = QtWidgets.QLabel("NULL", self)
        self.name_company.setGeometry(QtCore.QRect(470, 50, 400, 13))

        self.label_5 = QtWidgets.QLabel("Зарплата:", self)
        self.label_5.setGeometry(QtCore.QRect(470, 66, 61, 20))

        self.label_6 = QtWidgets.QLabel("Требуемый опыт работы:", self)
        self.label_6.setGeometry(QtCore.QRect(470, 90, 141, 16))

        self.salary = QtWidgets.QLabel("NULL", self)
        self.salary.setGeometry(QtCore.QRect(530, 70, 247, 13))

        self.experience = QtWidgets.QLabel("NULL", self)
        self.experience.setGeometry(QtCore.QRect(610, 90, 247, 16))

        self.label_7 = QtWidgets.QLabel("Город:", self)
        self.label_7.setGeometry(QtCore.QRect(470, 110, 41, 21))

        self.city = QtWidgets.QLabel("NULL", self)
        self.city.setGeometry(QtCore.QRect(510, 110, 247, 21))

        self.date = QtWidgets.QLabel("NULL", self)
        self.date.setGeometry(QtCore.QRect(570, 130, 65, 21))

        self.label_8 = QtWidgets.QLabel("Дата размещения:", self)
        self.label_8.setGeometry(QtCore.QRect(470, 130, 101, 21))

        self.tabWidget.setCurrentIndex(0)
        self.resize(452, 400)
        self.setWindowTitle('Просмотр вакансий')
        self.show()
        self.center()
        self.load_data()

    def load_vacancy_info(self, index):
        vacancy = self.conn.vacancy_show(index)
        vacancy_location = self.conn.vacancy_show_location(index)
        vacancy_req = self.conn.vacancy_show_req(index)
        vacancy_exp = self.conn.vacancy_show_exp(index)
        vacancy_con = self.conn.vacancy_show_con(index)
        if vacancy == None:
            vacancy = self.conn.vacancy_show_error(index)
            name_vacancy = str(vacancy[1])
            name_company = str(vacancy[2])
            city = str(vacancy_location[1])
            metro = str(vacancy_location[2])
            experience = str(vacancy[3])
            location = ''
            if metro == 'Отсутствует информация':
                location = city
            else:
                location = city + ', ' + metro
            _salary = 'Отсутствует информация'
            date = str(vacancy[4])
            if date == None:
                date = 'Отсутствует информация'
            url = str(vacancy[5])
        else:
            name_vacancy = str(vacancy[1])
            name_company = str(vacancy[2])
            city = str(vacancy_location[1])
            metro = str(vacancy_location[2])
            experience = str(vacancy[5])
            location = ''
            if metro == 'Отсутствует информация':
                location = city
            else:
                location = city + ', ' + metro
            salary = str(vacancy[3])
            currency = str(vacancy[4])
            _salary = str(vacancy[3]) + " " + str(vacancy[4])
            date = str(vacancy[6])
            if date == None:
                date = 'Отсутствует информация'
            url = str(vacancy[7])
        self.name_vacancy.setText(name_vacancy)
        self.name_company.setText(name_company)
        self.city.setText(location)
        self.salary.setText(_salary)
        self.experience.setText(experience)
        self.date.setText(date)
        self.url = url
        model_req = QtGui.QStandardItemModel()
        model_con = QtGui.QStandardItemModel()
        model_exp = QtGui.QStandardItemModel()
        if vacancy_req != None:
            for key in vacancy_req:
                item = QtGui.QStandardItem(str(key[0]))
                item.setEditable(False)
                model_req.appendRow(item)
        if vacancy_con != None:
            for key in vacancy_con:
                item = QtGui.QStandardItem(str(key[0]))
                item.setEditable(False)
                model_con.appendRow(item)
        if vacancy_exp != None:
            for key in vacancy_exp:
                item = QtGui.QStandardItem(str(key[0]))
                item.setEditable(False)
                model_exp.appendRow(item)
        self.tableView_2.setModel(model_req)
        self.tableView_2.setColumnWidth(0, 330)
        self.tableView_3.setModel(model_exp)
        self.tableView_3.setColumnWidth(0, 330)
        self.tableView_4.setModel(model_con)
        self.tableView_4.setColumnWidth(0, 330)
        self.resize(812, 400)

    def open_browser(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.url))

    def load_data(self):
        model = QtGui.QStandardItemModel()
        model.setColumnCount(4)
        headerNames = []
        headerNames.append("ID")
        headerNames.append("Имя вакансии")
        headerNames.append("Компания")
        headerNames.append("Дата")
        model.setHorizontalHeaderLabels(headerNames)
        try:
            vacancy_list = self.conn.vacancies_show(self.index)
            for row in vacancy_list:
                row_data = []
                i = 0
                for key in row:
                    if str(key) == "None":
                        item = QtGui.QStandardItem(str("Не указано"))
                        item.setEditable(False)                        
                    else:
                        item = QtGui.QStandardItem(str(key))
                        item.setEditable(False)
                    row_data.append(item)
                    i += 1
                model.appendRow(row_data)
            self.tableView.setModel(model)
            self.tableView.setColumnWidth(0, 40)
            self.tableView.setColumnWidth(1, 155)
            self.tableView.setColumnWidth(2, 105)
            self.tableView.setColumnWidth(3, 70)
        except:
            QtWidgets.QMessageBox.warning(self, 'Ошибка!', 'Ошибка при загрузке таблицы!', QtWidgets.QMessageBox.Ok)       

    def show_all_info(self):
        try:
            index = self.tableView.selectedIndexes()
            self.load_vacancy_info(index[0].data())
        except:
            QtWidgets.QMessageBox.warning(self, 'Ошибка!', 'Выберите строку с вакансией!', QtWidgets.QMessageBox.Ok)
    
    def undo_all_info(self):
        self.resize(452, 400)
    
    def center(self):
        fr_geo = self.frameGeometry()
        center = QtWidgets.QDesktopWidget().availableGeometry().center()
        fr_geo.moveCenter(center)
        self.move(fr_geo.topLeft())