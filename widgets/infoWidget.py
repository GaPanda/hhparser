from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QFont

class InfoWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initWidget()
    
    def initWidget(self):
        self.label = QLabel('''<html><head/><body><p align=\"center\">
                                      <span style=\" font-size:10pt;\">Программа для парсинга https://hh.ru</span></a></p>
                                      <p align=\"center\">
                                      <span style=\" font-size:10pt;\">Для работы программы требуется подключение к интернету.</span></a></p>
                                      <p align=\"center\">
                                      <span style=\" font-size:10pt;\">GitHub: https://github.com/GaPanda/hhparser</span></p>
                                      </body></html>''', self)
        self.label.setGeometry(QRect(0, 120, 500, 100))