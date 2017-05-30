import time

from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QMessageBox,
                             QMenuBar, QDesktopWidget, QApplication, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QProgressBar, QFileDialog)
from PyQt5.QtCore import QCoreApplication, QRect, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QFont
from libs.hh_parse import SearchQuery
from libs.hh_config import Data
from libs.hh_mssql import MssqlConnection

class Worker(QObject):
    sig_step = pyqtSignal(int, int)
    sig_query = pyqtSignal(int, str)
    sig_done = pyqtSignal()
    sig_error = pyqtSignal(str)
    sig_progress = pyqtSignal(int)
    sig_msg = pyqtSignal(str)
    sig_time = pyqtSignal(int)

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.search_time_start = 0
        self.search_time = 0
        self.vacancy_count = 0
        self.vacancy_analized = 0
        self.queries_number = 0
        self.cur_query = 0
        self.progress = 0

    def vacancy_count_func(self, value):
        self.vacancy_count = value
        self.search_time_cur_func()

    def search_time_start_func(self):
        self.search_time_start = time.time()
    
    def vacancy_analized_func(self, value):
        self.vacancy_analized = value
        self.sig_step.emit(self.vacancy_count, self.vacancy_analized)
        self.search_time_cur_func()
        progress = self.progress + float((self.vacancy_analized / self.vacancy_count) * (1 / self.queries_number)*100)
        print(progress)
        self.sig_progress.emit(progress)
    
    def search_time_cur_func(self):
        cur_search_time = int(time.time() - self.search_time_start)
        self.sig_time.emit(cur_search_time)
    
    def search_time_end_func(self):
        self.search_time = int(time.time() - self.search_time_start)
        self.sig_time.emit(self.search_time)

    def set_number_queries(self, value):
        self.queries_number = value

    def set_progress(self, value):
        self.progress = value
        self.sig_progress.emit(int(self.progress))

    @pyqtSlot()
    def work(self):
        #SearchQuery
        self.config = Data()
        self.config.load_from_conf()
        try:
            self.queries_names = self.open_file()
        except:
            self.sig_error.emit('Невозможно открыть файл.')
            print(u'\nНевозможно открыть файл.')
            return
        self.queries = []
        self.set_number_queries(len(self.queries_names))
        i = 1
        self.cur_query = i
        for query in self.queries_names:
            try:
                self.sig_query.emit(i, query)
                self.sig_time.emit(0)
                self.sig_step.emit(0,0)
                self.sig_msg.emit('Обработка запроса : {0}'.format(query))
                self.search_time_start_func()
                self.query_object = SearchQuery()
                self.query_object.vacancy_count_signal.connect(self.vacancy_count_func)
                self.query_object.vacancy_analized_signal.connect(self.vacancy_analized_func)
                self.query_object.query_finished_signal.connect(self.search_time_end_func)
                self.query_object.query_finished_signal.connect(self.add_into_list)                
                self.query_object.set_query_config(query, self.config.rtimeout(), self.config.rrequirments(), self.config.rexpectations(), self.config.rconditions())
                self.sig_msg.emit('Обработка запроса...')
                self.search_time_cur_func()
                self.query_object.start_search()
                self.sig_msg.emit('Обработка вакансий...')
                self.query_object.get_vacancy_information(self.search_time_start)
                self.set_progress((i / self.queries_number)*100)
            except Exception as inst:
                self.set_progress((i / self.queries_number)*100)
                self.sig_msg.emit('{0}'.format(inst))
                print(inst)
            except:
                self.set_progress((i / self.queries_number)*100)
                self.sig_msg.emit('Непредвиденная ошибка, выполнение запроса будет остановлено!')
                print(u'Непредвиденная ошибка, выполнение запроса будет остановлено!')
            i += 1
            self.cur_query = i
        if self.queries:
            self.sig_done.emit()
        else:
            self.sig_error.emit('Нету данных для добавления в БД.')

    def add_into_list(self):
        self.queries.append(self.query_object)

    def open_file(self):
        file = open(self.filepath)
        queries_names = []
        for line in file:
            queries_names.append(line)
        return queries_names

    def add_into_database(self):
        if self.queries:
            conn = MssqlConnection(self.config.rserver_name(), self.config.rdb_name(), self.config.rusername(), self.config.rpassword())
            conn_result = conn.check_connection()
            try:
                for query in self.queries:
                    self.sig_msg.emit('Добавление {0} в базу данных.'.format(query.search_text))               
                    print(u'Добавление {0} в базу данных.'.format(query.search_text))
                    conn.insert_all_data(query)
                self.sig_msg.emit('Добавление {} запроса(ов) успешно завершено.'.format(str(len(self.queries))))
                print(u'Добавление успешно завершено.')
            except Exception as inst:
                self.sig_error.emit('{0}'.format(inst))
                print(inst)
            except:
                self.sig_error.emit('Непредвиденная ошибка')
                print(u'Непредвиденная ошибка')
        else:
            self.sig_error.emit('Нету данных для добавления в базу данных!')
            print(u'Нету данных для добавления в базу данных!')

class SearchFileWidget(QWidget):

    sig_add_in_db = pyqtSignal()
    sig_work = pyqtSignal(bool)

    def __init__(self, bar, active):
        super().__init__()
        self.initWidget()
        self.status_bar = bar
        self.active = active

    def initWidget(self):
        #Labels
        self.search_file = QLabel('Файл с запросами: ', self)
        self.search_file.setGeometry(QRect(30, 40, 131, 16))
        self.progress_text = QLabel('Прогресс: ', self)
        self.progress_text.setGeometry(QRect(30, 70, 131, 21))
        self.time_label_name = QLabel('Время обработки: ', self)
        self.time_label_name.setGeometry(QRect(30, 160, 131, 16))
        self.time_label = QLabel('{} сек'.format(0), self)
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
        self.query_text_value = QLabel("Пусто", self)
        self.query_text_value.setGeometry(QRect(190, 130, 200, 16))
        self.name = QLabel('Поиск вакансий с загрузкой запросов из файла', self)
        self.name.setGeometry(QRect(10, 10, 241, 16))
        font = QFont()
        font.setPointSize(10)
        self.name.setFont(font)
        self.file_text = QLabel('', self)
        self.file_text.setGeometry(QRect(190, 40, 271, 21))
        self.file_text.setVisible(False)
        #LineEdits
        self.search_file_edit = QLineEdit(self)
        self.search_file_edit.setGeometry(QRect(190, 40, 191, 21))
        #Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(QRect(190, 70, 271, 23))
        self.progress_bar.setProperty("value", 0)
        #Buttons
        self.search_button = QPushButton('Поиск', self)
        self.search_button.setGeometry(QRect(390, 250, 75, 23))
        self.search_button.clicked.connect(self.search_button_clicked)
        self.new_query_button = QPushButton('Новый запрос', self)
        self.new_query_button.setGeometry(QRect(300, 250, 85, 23))
        self.new_query_button.clicked.connect(self.new_query_button_clicked)
        self.file_open_button = QPushButton('Открыть', self)
        self.file_open_button.setGeometry(QRect(390, 40, 71, 21))
        self.file_open_button.clicked.connect(self.file_open_button_clicked)
        self.new_query_button.setEnabled(False)

        QThread.currentThread().setObjectName('search_file_widget')

    def search_button_clicked(self):
        if not self.active:
            self.sig_work.emit(True)
            text = str(self.search_file_edit.text())
            self.file_text.setText(text)
            self.file_text.setVisible(True)
            self.search_file_edit.setVisible(False)
            self.search_button.setEnabled(False)
            self.file_open_button.setVisible(False)
            self.__threads = []
            worker = Worker(text)
            thread = QThread()
            thread.setObjectName('query_file_thread')
            self.__threads.append((thread, worker))
            worker.moveToThread(thread)

            worker.sig_step.connect(self.on_worker_step)
            worker.sig_done.connect(self.on_worker_done)
            worker.sig_progress.connect(self.progress_step)
            worker.sig_error.connect(self.error_msg)
            worker.sig_msg.connect(self.info_msg)
            worker.sig_time.connect(self.set_query_time)
            worker.sig_query.connect(self.query_data)

            self.sig_add_in_db.connect(worker.add_into_database)

            thread.started.connect(worker.work)
            thread.start()
        else:
            QMessageBox.warning(self, 'Ошибка!', 'Поиск вакансий уже запущен!', QMessageBox.Ok)

    def new_query_button_clicked(self):
        self.new_query_button.setEnabled(False)
        self.search_button.setEnabled(True)
        self.status_bar.showMessage('Готов!')
        self.file_text.setText('')
        self.time_label.setText('{} секунд'.format(0))
        self.progress_bar.setValue(0)
        self.search_file_edit.setText('')
        self.vacancy_analized_number.setText('0')
        self.vacancy_count_number.setText('0')
        self.query_text_value.setText('Пусто')
        self.number_query_value.setText('0')
        self.file_text.setVisible(False)
        self.search_file_edit.setVisible(True)
        self.file_open_button.setVisible(True)
   
    def file_open_button_clicked(self):
        file_name = QFileDialog.getOpenFileName(self, 'Открыть файл')[0]
        self.search_file_edit.setText(file_name)

    @pyqtSlot(bool)
    def status_changed(self, status: bool):
        self.active = status

    @pyqtSlot(int, str)
    def query_data(self, query_number: int, query_name: str):
        self.number_query_value.setText(str(query_number))
        self.query_text_value.setText(query_name.strip())
    @pyqtSlot(int, int)
    def on_worker_step(self, v_c: int, v_a: int):
        self.vacancy_analized_number.setText(str(v_a))
        self.vacancy_count_number.setText(str(v_c))

    @pyqtSlot(int)
    def progress_step(self, value: int):
        self.progress_bar.setValue(value)

    @pyqtSlot(str)
    def error_msg(self, message: str):
        self.status_bar.showMessage(message)
        QMessageBox.warning(self, 'Ошибка!', message, QMessageBox.Ok)
        self.new_query_button.setEnabled(True)
        for thread, worker in self.__threads:
            thread.quit()
            thread.wait()
            self.__threads.pop()
        self.sig_work.emit(False)

    @pyqtSlot(str)
    def info_msg(self, message: str):
        self.status_bar.showMessage(message)

    @pyqtSlot(int)
    def set_query_time(self, sec: int):
        self.time_label.setText('{} секунд'.format(sec))

    @pyqtSlot()
    def on_worker_done(self):
        self.config = Data()
        self.config.load_from_conf()
        self.status_bar.showMessage('Установка соединения с базой данных...')
        conn = MssqlConnection(self.config.rserver_name(), self.config.rdb_name(), self.config.rusername(), self.config.rpassword())
        conn_result = conn.check_connection()        
        if conn_result == 1:
            reply = QMessageBox.question(self, 'Добавление в Базу данных',
                                        "Хотите добавить запрос в базу данных?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.sig_add_in_db.emit()
            else:
                self.status_bar.showMessage('Операция добавления отменена.')
            for thread, worker in self.__threads:
                thread.quit()
                thread.wait()
                self.__threads.pop()
            self.new_query_button.setEnabled(True)
            self.search_button.setEnabled(False)
        else:
            self.error_msg('Соединение с базой не установлено.')
            print(u'Соединение с базой не установлено.')
        self.sig_work.emit(False)