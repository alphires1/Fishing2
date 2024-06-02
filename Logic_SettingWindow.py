from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6 import QtCore
import FishingTools
from UI_SettingWindow import Ui_SettingWindow
from PyQt6.QtGui import QCloseEvent, QMovie
from pynput.keyboard import Listener


class SettingWindow(QMainWindow):
    _instance = None
    data_returned = QtCore.pyqtSignal(str, str)  # 设置一个信号供观察者监测
    
    def __init__(self, main_window):  # 设置窗口一定是被主窗口的设置按钮实例化的， 传参的同时也避免导入主窗口类使用导致耦合度过高
        super().__init__()
        self.tool = FishingTools.Tool.get_instance()
        self.key_str = ""
        # 设置窗口UI部分
        self.ui = Ui_SettingWindow()
        self.main_window = main_window
        self.ui.setupUi(self)
        self.setFixedSize(300, 200)
        self.movie = QMovie("./resources/bg_1.gif")
        self.ui.bg_label.setMovie(self.movie)  # 设置背景Label
        self.movie.start()
        self.setWindowFlags(self.windowFlags().WindowCloseButtonHint)  # 禁用最小化按钮?? 为什么不是WindowMinimizeButtonHint

        self.config_dict = self.main_window.config_dict  # 获取配置信息
        """根据配置信息设置UI"""
        self.ui.collect_toolButton.setText(self.config_dict['收藏'])
        self.ui.sale_toolButton.setText(self.config_dict['出售'])
        self.ui.throw_toolButton.setText(self.config_dict['抛竿'])
        self.bg_path = self.config_dict['主窗口背景']
        print("[bg_main]开始获取列表")
        self.bg_path_list = self.tool.get_img_arr(self, "bg_main")

        self.bg_radioButton_list = [
            self.ui.bg_radioButton,
            self.ui.bg_radioButton_2,
            self.ui.bg_radioButton_3,
            self.ui.bg_radioButton_4,
        ]
        i = 0
        while i < len(self.bg_path_list):
            if self.bg_path == self.bg_path_list[i]:
                self.bg_radioButton_list[i].setChecked(True)  # 设置初始被选中的按钮
                break
            i += 1

        # 信号绑定
        self.ui.bg_radioButton.clicked.connect(self.on_radioButton_clicked)
        self.ui.bg_radioButton_2.clicked.connect(self.on_radioButton2_clicked)
        self.ui.bg_radioButton_3.clicked.connect(self.on_radioButton3_clicked)
        self.ui.bg_radioButton_4.clicked.connect(self.on_radioButton4_clicked)
        self.data_returned.connect(self.tool.on_data_returned)
        self.ui.collect_toolButton.clicked.connect(self.on_collect_clicked)
        self.ui.sale_toolButton.clicked.connect(self.on_sale_clicked)
        self.ui.throw_toolButton.clicked.connect(self.on_throw_clicked)

    # 单例
    @classmethod
    def get_instance(cls, main_window):
        if cls._instance is None:
            cls._instance = SettingWindow(main_window)
        return cls._instance

    def closeEvent(self, event: QCloseEvent) -> None:
        """重载关闭函数，准备用于对象池优化"""
        self.main_window.ui.setting_toolButton.setEnabled(True)
        event.ignore()
        self.hide()

    def set_center_pos(self, widget: QWidget):
        new_pos_x = widget.pos().x() + widget.width() // 2 - self.width() // 2
        new_pos_y = widget.pos().y() + widget.height() // 2 - self.height() // 2
        new_rect = QtCore.QRect(new_pos_x, new_pos_y, (widget.width()), (widget.height()))
        self.setGeometry(new_rect)

    def on_radioButton_clicked(self):
        self.data_returned.emit('主窗口背景', self.bg_path_list[0])

    def on_radioButton2_clicked(self):
        self.data_returned.emit('主窗口背景', self.bg_path_list[1])

    def on_radioButton3_clicked(self):
        self.data_returned.emit('主窗口背景', self.bg_path_list[2])

    def on_radioButton4_clicked(self):
        self.data_returned.emit('主窗口背景', self.bg_path_list[3])

    def on_collect_clicked(self):
        with Listener(on_press=self.begin_listen, on_release=self.end_listen) as listener:
            listener.join()
        self.data_returned.emit("收藏", self.key_str)
        self.ui.collect_toolButton.setText(self.key_str)

    def on_sale_clicked(self):
        with Listener(on_press=self.begin_listen, on_release=self.end_listen) as listener:
            listener.join()
        self.data_returned.emit("出售", self.key_str)
        self.ui.sale_toolButton.setText(self.key_str)

    def on_throw_clicked(self):
        with Listener(on_press=self.begin_listen, on_release=self.end_listen) as listener:
            listener.join()
        self.data_returned.emit("抛竿", self.key_str)
        self.ui.throw_toolButton.setText(self.key_str)

    def begin_listen(self, key):
        try:
            self.key_str = format(key.char)
            print(key.char)
        except AttributeError:
            temp = format(key)
            i = 0
            for char in temp:
                i += 1
                if i > 4:
                    self.key_str = self.key_str + char

    def end_listen(self, key):
        self.setEnabled(True)
        self.ui.tips_label.setText(QtCore.QCoreApplication.translate("SettingWindow",
                                                                     "<html><head/><body><p><span style=\" "
                                                                     "color:#26f717;\">请按游戏中规则绑定对应按键</span></p></body"
                                                                     "></html>"))
        return False
