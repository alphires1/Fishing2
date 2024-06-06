from PyQt6.QtWidgets import QMainWindow
from UI_MainWindow import Ui_Form
from Logic_SettingWindow import SettingWindow
from PyQt6 import QtCore
import FishingTools
from Logic_Fishing import Fishing
import time


# 主窗口逻辑类
class MainWindow(QMainWindow):
    operation_state = QtCore.pyqtSignal(str)

    def __init__(self, app):
        super().__init__()
        # 实例化主窗口
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.fishing = Fishing.get_instance(self)
        self.fishing_tool = FishingTools.Tool.get_instance()  # 获取工具类 准备加载配置
        # self.config_dict = self.fishing_tool.config_dict  无意义，后续变动后主进程不会再次获取

        # 配置主窗口属性
        self.setFixedSize(710, 400)  # 锁定主窗口大小

        """将窗口坐标置于屏幕中心,虽然不这么做窗口也可能会被系统自动置中，但对于窗口自身，他的坐标却没有变化"""
        self.screen = app.primaryScreen()
        self.screen_center_pos = FishingTools.Pos(self.screen.size().width() // 2 - self.width() // 2,
                                                  self.screen.size().height() // 2 - self.height() // 2)
        self.setGeometry(self.screen_center_pos.x, self.screen_center_pos.y, self.width(), self.height())
        # 配置控件属性
        self.ui.operationText.setFixedSize(300, 200)
        self.bg_pixmap = self.fishing_tool.get_img(self.fishing_tool.config_dict['主窗口背景'])
        self.ui.bgLabel.setPixmap(self.bg_pixmap)
        # self.ui.bgLabel
        self.setting_window = SettingWindow.get_instance(self)
        self.setting_window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)  # 设置为模态
        # 信号绑定
        self.ui.start_button.clicked.connect(self.on_start_clicked)
        self.ui.stop_button.clicked.connect(self.on_stop_clicked)
        self.ui.stop_button.setEnabled(False)
        self.ui.setting_toolButton.clicked.connect(self.show_setting_window)
        self.setting_window.data_returned.connect(self.on_data_returned)
        self.operation_state.connect(self.fishing.on_state_changed)

        # 异步线程，防止阻滞主线程
        """设置后台线程"""
        self.fishiing_worker = FishingTools.Worker(self.on_fishing_start)
        self.fishiing_worker.signals.result.connect(self.on_fishing_result)
        self.fishiing_worker.signals.finish.connect(self.on_fishing_finished)
        self.fishiing_worker.signals.error.connect(self.on_fishing_error)

        self.fishing_throw = FishingTools.Worker(self.on_fishing_throw)
        self.fishing_throw.signals.result.connect(self.on_fishing_result)
        self.fishing_throw.signals.error.connect(self.on_fishing_error)

        self.keyboard_listener = FishingTools.KeyboardListener()
        self.keyboard_listener.key_pressed.connect(self.on_keyboard_start)

        #  开始后台任务
        self.fishiing_worker.start()
        self.fishing_throw.start()
        self.keyboard_listener.start()

    def on_fishing_start(self):
        # 这里是包含autogui的后台任务
        # 注意：不要在这里更新GUI，只处理数据或执行后台操作
        while True:
            msg = self.fishing.fishing_start()
            # 发射信号来更新GUI
            self.fishiing_worker.signals.result.emit(msg)
            time.sleep(0.1)

    def on_fishing_result(self, msg):
        # 在主线程中处理结果并更新GUI
        if msg is not None:
            self.update_operation_text(msg)

    def on_fishing_finished(self):
        pass

    def on_fishing_error(self, value):
        print(f"注意进程出错{value}")
        pass

    def on_fishing_returned(self, msg_type, msg):
        """用于接收功能逻辑传回的数据，异步线程避免阻滞主线程更新 """
        if msg_type == '更新文本':
            self.update_operation_text(msg)

    def on_fishing_throw(self):
        while True:
            msg = self.fishing.fishing_throw()
            self.fishing_throw.signals.result.emit(msg)
            time.sleep(0.1)

    def on_start_clicked(self):
        self.operation_state.emit('开始运行')
        self.update_operation_text('开始程序')
        self.ui.stop_button.setEnabled(True)
        self.ui.start_button.setEnabled(False)
        self.ui.setting_toolButton.setEnabled(False)

    def on_stop_clicked(self):
        self.operation_state.emit('停止运行')
        self.update_operation_text('停止程序')
        self.ui.stop_button.setEnabled(False)
        self.ui.start_button.setEnabled(True)
        self.ui.setting_toolButton.setEnabled(True)

    def on_data_returned(self, key, value):
        """观察者模式：监测设置窗口传回的值"""
        if key == '主窗口背景':
            print(f"修改{key}为：{value}")
            self.bg_pixmap = FishingTools.Tool.get_img(value)
            self.ui.bgLabel.setPixmap(self.bg_pixmap)

    def show_setting_window(self):
        """激活设置窗口"""
        self.setting_window.set_center_pos(self)
        self.setting_window.raise_()  # 将设置窗口置于顶部
        self.setting_window.activateWindow()  # 激活设置窗口
        self.setting_window.show()

    def update_operation_text(self, msg):
        """更新操作文本框"""
        self.ui.operationText.appendPlainText(msg)

    def on_keyboard_start(self, key):
        """监听键盘的后台线程"""
        print(f"按下了{key}")
        if key == self.fishing_tool.config_dict['开始']:
            self.on_start_clicked()
        elif key == self.fishing_tool.config_dict['停止']:
            self.on_stop_clicked()
            
    def on_listener_error(self, value: ValueError):
        print(value)
