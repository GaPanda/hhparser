from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QMessageBox,
                             QMenuBar, QDesktopWidget, QApplication, QLabel, QLineEdit,
                             QPlainTextEdit, QGridLayout, QProgressBar)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QRect, pyqtSlot
from PyQt5.QtGui import QIcon, QFont
from libs.hh_config import Data
from libs.hh_mssql import MssqlConnection

class SearchSettingsWidget(QWidget):
    def __init__(self, active):
        super().__init__()
        self.initWidget()
        self.active = active

    def initWidget(self):
        #Buttons
        self.save_button = QPushButton('Сохранить', self)
        self.save_button.setGeometry(QRect(280, 310, 81, 23))
        self.save_button.clicked.connect(self.set_config)
        self.cancel_button = QPushButton('Отмена', self)
        self.cancel_button.setGeometry(QRect(370, 310, 81, 23))
        self.cancel_button.clicked.connect(self.load_config)      
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
        self.expectations.setGeometry(QRect(40, 150, 101, 21))
        self.conditions = QLabel('Условия: ', self)
        self.conditions.setGeometry(QRect(40, 230, 101, 21))
        #LineEdits
        self.timeout_edit = QLineEdit(self)
        self.timeout_edit.setGeometry(QRect(210, 40, 241, 21))
        self.requirments_edit = QPlainTextEdit(self)
        self.requirments_edit.setGeometry(QRect(210, 70, 241, 71))
        self.expectations_edit = QPlainTextEdit(self)
        self.expectations_edit.setGeometry(QRect(210, 150, 241, 71))
        self.conditions_edit = QPlainTextEdit(self)
        self.conditions_edit.setGeometry(QRect(210, 230, 241, 71))
        #Classes
        self.config = Data()
        self.load_config()

    def load_config(self):
        try:
            self.config.load_from_conf()
            self.timeout_edit.setText(str(self.config.rtimeout()))
            self.requirments_edit.setPlainText(self.config.list_to_string(self.config.rrequirments()))
            self.expectations_edit.setPlainText(self.config.list_to_string(self.config.rexpectations()))
            self.conditions_edit.setPlainText(self.config.list_to_string(self.config.rconditions()))
        except:
            QMessageBox.warning(self, 'Ошибка!', 'Ошибка при загрузке config.ini!', QMessageBox.Ok)
    
    def set_config(self):
        if not self.active:
            try:
                timeout = float(self.timeout_edit.text())
                requirments = self.requirments_edit.toPlainText()
                expectations = self.expectations_edit.toPlainText()
                conditions = self.conditions_edit.toPlainText()
                self.config.ps_to_conf(timeout, requirments, conditions, expectations)
                self.config.write_query_to_conf()
                self.config.load_from_conf()
            except:
                QMessageBox.warning(self, 'Ошибка!', 'Ошибка при сохранении config.ini!', QMessageBox.Ok)
        else:
            QMessageBox.warning(self, 'Ошибка!', 'Дождитесь пока завершится поиск!', QMessageBox.Ok)

    @pyqtSlot(bool)
    def status_changed(self, status: bool):
        self.active = status