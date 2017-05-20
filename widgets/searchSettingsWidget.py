from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QStatusBar,
                             QMenuBar, QDesktopWidget, QApplication, QLabel, QLineEdit,
                             QPlainTextEdit, QGridLayout, QProgressBar)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QRect
from PyQt5.QtGui import QIcon, QFont

class SearchSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        #Buttons
        self.save_button = QPushButton('Сохранить', self)
        self.save_button.setGeometry(QRect(280, 250, 81, 23))
        self.cancel_button = QPushButton('Отмена', self)
        self.cancel_button.setGeometry(QRect(370, 250, 81, 23))        
        #Labels
        self.label = QLabel('Настройка параметров запроса', self)
        self.label.setGeometry(QRect(10, 10, 241, 16))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.timeout = QLabel('Тайм-аут между запросами: ', self)
        self.timeout.setGeometry(QRect(40, 40, 151, 21))
        self.requirments = QLabel('Требования: ', self)
        self.requirments.setGeometry(QRect(40, 70, 101, 21))
        self.expectations = QLabel('Ожидания: ', self)
        self.expectations.setGeometry(QRect(40, 130, 101, 21))
        self.conditions = QLabel('Условия: ', self)
        self.conditions.setGeometry(QRect(40, 190, 101, 21))
        #LineEdits
        self.timeout_edit = QLineEdit(self)
        self.timeout_edit.setGeometry(QRect(210, 40, 241, 21))
        self.requirments_edit = QPlainTextEdit(self)
        self.requirments_edit.setGeometry(QRect(210, 70, 241, 51))
        self.expectations_edit = QPlainTextEdit(self)
        self.expectations_edit.setGeometry(QRect(210, 130, 241, 51))
        self.conditions_edit = QPlainTextEdit(self)
        self.conditions_edit.setGeometry(QRect(210, 190, 241, 51))
 