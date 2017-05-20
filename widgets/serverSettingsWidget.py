       
from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QStatusBar,
                             QMenuBar, QDesktopWidget, QApplication, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QProgressBar)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QRect
from PyQt5.QtGui import QIcon, QFont

class ServerSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        #Buttons
        self.save_button = QPushButton('Сохранить', self)
        self.save_button.setGeometry(QRect(280, 160, 81, 23))
        self.cancel_button = QPushButton('Отмена', self)
        self.cancel_button.setGeometry(QRect(370, 160, 81, 23))
        self.test_button = QPushButton('Проверка соединения', self)
        self.test_button.setGeometry(QRect(150, 160, 121, 23))
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
        self.user_name = QLabel('Пользователь: ', self)
        self.user_name.setGeometry(QRect(40, 70, 101, 21))
        self.user_password = QLabel('Пароль: ', self)
        self.user_password.setGeometry(QRect(40, 100, 101, 21))
        #LineEdits
        self.server_name_edit = QLineEdit(self)
        self.server_name_edit.setGeometry(QRect(210, 40, 241, 21))
        self.database_name_edit = QLineEdit(self)
        self.database_name_edit.setGeometry(QRect(210, 70, 241, 21))
        self.user_name_edit = QLineEdit(self)
        self.user_name_edit.setGeometry(QRect(210, 100, 241, 21))
        self.user_password_edit = QLineEdit(self)
        self.user_password_edit.setGeometry(QRect(210, 130, 241, 21))
        