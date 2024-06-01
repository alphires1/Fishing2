from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import pyqtSignal
from UI_SettingWindow import Ui_SettingWindow
from Logic_MainWindow import MainWinow
class SettingWindow(QMainWindow):
    _instance = None
    data_returned = pyqtSignal(str, str)  # 设置一个信号供观察者监测

    def __init__(self, mainwindow):
        super().__init__()
        self. settingwindow = Ui_SettingWindow()
        self.mainwindow = mainwindow

        self.settingwindow.setupUi()
        self.setFixedSize(284, 184)
        self.pixmap = MainWinow.set_BgImg("./resources/bg_main_1.png")


    #单例
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SettingWindow(cls)
        return cls._instance
