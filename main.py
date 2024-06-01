import sys
from  PyQt6.QtWidgets import QApplication
from Logic_MainWindow import MainWinow


#主程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWinow()
    window.show()
    sys.exit(app.exec())