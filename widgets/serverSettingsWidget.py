       
from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QMessageBox,
                             QMenuBar, QDesktopWidget, QApplication, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QProgressBar)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QRect, pyqtSlot
from PyQt5.QtGui import QIcon, QFont
from libs.hh_config import Data
from libs.hh_mssql import MssqlConnection

class ServerSettingsWidget(QWidget):
    def __init__(self, active):
        super().__init__()
        self.initWidget()
        self.active = active

    def initWidget(self):
        #Buttons
        self.save_button = QPushButton('Сохранить', self)
        self.save_button.setGeometry(QRect(280, 160, 81, 23))
        self.save_button.clicked.connect(self.set_config)
        self.cancel_button = QPushButton('Отмена', self)
        self.cancel_button.setGeometry(QRect(370, 160, 81, 23))
        self.cancel_button.clicked.connect(self.load_config)
        self.test_button = QPushButton('Проверка соединения', self)
        self.test_button.setGeometry(QRect(150, 160, 121, 23))
        self.test_button.clicked.connect(self.check_db)
        #Labels
        self.label = QLabel('Настройка сервера и базы данных', self)
        self.label.setGeometry(QRect(10, 10, 241, 16))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.server_name = QLabel('Имя сервера: ', self)
        self.server_name.setGeometry(QRect(40, 40, 101, 21))
        self.database_name = QLabel('Имя базы данных: ', self)
        self.database_name.setGeometry(QRect(40, 130, 101, 21))
        self.user_name = QLabel('Пользователь(не обязательно): ', self)
        self.user_name.setGeometry(QRect(40, 70, 190, 21))
        self.user_password = QLabel('Пароль(не обязательно): ', self)
        self.user_password.setGeometry(QRect(40, 100, 150, 21))
        #LineEdits
        self.server_name_edit = QLineEdit(self)
        self.server_name_edit.setGeometry(QRect(230, 40, 221, 21))
        self.database_name_edit = QLineEdit(self)
        self.database_name_edit.setGeometry(QRect(230, 130, 221, 21))
        self.user_name_edit = QLineEdit(self)
        self.user_name_edit.setGeometry(QRect(230, 70, 221, 21))
        self.user_password_edit = QLineEdit(self)
        self.user_password_edit.setGeometry(QRect(230, 100, 221, 21))
        #Classes
        self.config = Data()
        self.load_config()
    
    def load_config(self):
        try:
            self.config.load_from_conf()
            self.server_name_edit.setText(self.config.rserver_name())
            self.database_name_edit.setText(self.config.rdb_name())
            self.user_name_edit.setText(self.config.rusername())
            self.user_password_edit.setText(self.config.rpassword())
        except:
            QMessageBox.warning(self, 'Ошибка!', 'Ошибка при загрузке config.ini!', QMessageBox.Ok)
    
    def set_config(self):
        if not self.active:
            try:
                server_name = str(self.server_name_edit.text())
                db_name = str(self.database_name_edit.text())
                username = str(self.user_name_edit.text())
                password = str(self.user_password_edit.text())
                self.config.dbs_to_conf(db_name, server_name, username, password)
                self.config.write_serv_to_conf()
                self.config.load_from_conf()
            except:
                QMessageBox.warning(self, 'Ошибка!', 'Ошибка при сохранении config.ini!', QMessageBox.Ok)
        else:
            QMessageBox.warning(self, 'Ошибка!', 'Дождитесь пока завершится поиск!', QMessageBox.Ok)

    def check_db(self):
        if not self.active:
            conn = MssqlConnection(self.config.rserver_name(), self.config.rdb_name(), self.config.rusername(), self.config.rpassword())
            print('Установка соединения с БД...\n')
            check = conn.check_connection()
            if check == 1:
                QMessageBox.information(self, 'Ок!', 'Соединение с сервером установлено!', QMessageBox.Ok)
                print(u'Соединение с сервером установлено!')
            else:
                QMessageBox.warning(self, 'Ошибка!', 'Соединение с сервером не установлено!', QMessageBox.Ok)
                print(u'Соединение с сервером не установлено!')
        else:
            QMessageBox.warning(self, 'Ошибка!', 'Дождитесь пока завершится поиск!', QMessageBox.Ok)

    @pyqtSlot(bool)
    def status_changed(self, status: bool):
        self.active = status