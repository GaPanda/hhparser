from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QPushButton, QStatusBar,
                             QMenuBar, QDesktopWidget, QApplication, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QProgressBar)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QRect
from PyQt5.QtGui import QIcon, QFont

class InfoWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initWidget()
    
    def initWidget(self):
        pass