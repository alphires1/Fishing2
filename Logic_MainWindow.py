from PyQt6.QtWidgets import QMainWindow
from UI_MainWindow import Ui_Form


#主窗口逻辑类
class MainWinow(QMainWindow):
    def __init__(self):
        super().__init__()
        _instance = None
        # 实例化主窗口
        self.mainwindow = Ui_Form()
        self.mainwindow.setupUi(self)
        # 配置主窗口属性
        self.setFixedSize(710, 400)  # 锁定主窗口大小
        # 配置控件属性
        self.mainwindow.operationText.setFixedSize(300, 200)
        # self.mainwindow.bgLabel

        # 信号绑定
        self.mainwindow.start_button.clicked.connect(self.on_start_clicked)
        self.mainwindow.stop_button.clicked.connect(self.on_stop_clicked)
        self.mainwindow.stop_button.setEnabled(False)
        self.mainwindow.setting_toolButton.clicked.connect(self.show_setting_window)

    def on_start_clicked(self):
        self.update_operation_text('开始程序')
    def on_stop_clicked(self):
        self.update_operation_text('停止程序')

    def show_setting_window(self):
        pass


    def update_operation_text(self, msg):
        """更新操作文本框"""
        self.ui.operationText.appendPlainText(msg)