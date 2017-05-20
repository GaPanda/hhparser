import sys
from PyQt5.QtWidgets import QApplication
from widgets.mainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main())