import io
import os
import json
import cv2
import time
import pyautogui as ag
import os
from PIL import Image
from PyQt6.QtWidgets import QWidget, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal, QObject, QThread
import Logic_Fishing, Logic_MainWindow, Logic_SettingWindow
from pynput.keyboard import Controller, Listener, Key


class Tool:
    _instance = None

    def __init__(self):
        super().__init__()
        self.config_path = "config.json"
        self.default_config_dict = {
            '主窗口背景': r".\resources\bg_main_1.png",
            "抛竿": 'f1',
            '收藏': 'f1',
            '出售': 'f1',
            '开始': 'home',
            '停止': 'end'
        }  # 默认配置
        self.fishing = Logic_Fishing.Fishing.get_instance(self)
        self.keyboard = Controller()
        self.key_str = ""
        self.is_emit = False
        self.config_dict = {}  # 配置字典
        self.chk_config_path(self.config_path)  # 检查配置文件
        self.load_setting_files(self.config_path)  # 加载配置

        """
            可以这么写，但逻辑不合理，工具类最好不与其他类发生交涉，仅提供函数使用
            同时，设置窗口应该在主窗口的逻辑里实例化     
        """
        # self.settingwindow = SettingWindow.get_instance()
        # self.setting_window.data_returned.connect(self.on_data_returned)  # 将信号函数与设置窗口发出的信号绑定

    @classmethod
    # 单例
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()  # 创建类的实例
        return cls._instance

    @staticmethod
    def get_img(path):
        """静态工具函数,从参数路径获取并返回图片数据"""
        with Image.open(path) as img:
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='PNG')
            byte_arr = byte_arr.getvalue()
            pixmap = QPixmap()
            pixmap.loadFromData(byte_arr)
            return pixmap

    @staticmethod
    def get_img_info(pic_name, deal_type='direct'):
        """静态工具函数"""
        name_arr = []
        path_arr = []
        # img_arr = []
        if deal_type == 'split':
            pic_name = pic_name.split('_')[0]
        img_path = os.path.join('.', 'resources', pic_name)
        temp_continue = True
        i = 1
        while temp_continue:
            pic_path = img_path + f"_{i}.png"
            name = pic_name + f"_{i}.png"
            img = Tool.load_img(pic_path)
            if img is None:
                print(f"载入{pic_path}失败")
                break
            print(f"{name}已载入")
            name_arr.append(name)
            #img_arr.append(img)
            path_arr.append(pic_path)
            i += 1
        print(f"共加载[{len(name_arr)}]张图片")
        img_info = Image_info(name_arr, path_arr)
        return img_info

    @staticmethod
    def load_img(pic_path):
        path = os.path.join(pic_path)
        try:
            image = cv2.imread(path)
            return image
        except FileNotFoundError as e:
            print("载入完毕")

    def on_data_returned(self, key, value):
        """信号函数，存储配置"""
        print(f"检测到数据修改，[{key}：{value}]已存储")
        self.config_dict[key] = value
        self.save_setting_files(self.config_path)

    # 加载本地配置：json格式
    def load_setting_files(self, path):
        """加载配置文件"""
        try:
            with open(path, 'r') as file:
                self.config_dict = json.load(file)
                print(f"正在加载配置文件 {path} ")
        except FileNotFoundError:
            print(f"配置文件 {path} 未找到，已重置为默认设置。")
            self.default_setting_files()
        except json.JSONDecodeError:
            print(f"配置文件 {path}格式错误，已重置为默认设置。")
            self.default_setting_files()
        except Exception as e:
            print(f"加载配置文件{path}时发生未知错误：{e}")
            self.default_setting_files()
        default_config_keys = set(self.default_config_dict)
        result = default_config_keys.issubset(self.config_dict.keys())  # 校验默认配置中的所有键是否都在当前配置文件中
        if not result:  # 如果缺少，则加载默认配置
            for key in default_config_keys:
                if self.config_dict.get(key) is None:
                    self.config_dict[key] = self.default_config_dict[key]

        print("具体配置如下：{")
        for key, value in self.config_dict.items():
            print(key + ":", value)
        print('}')

    def chk_config_path(self, path):
        """检查配置文件"""
        if not os.path.exists(path):
            print(f"配置文件 {path} 不存在，将创建默认配置。")
            self.default_setting_files()

    def default_setting_files(self):
        """将配置文件重置为默认配置"""
        self.config_dict = self.default_config_dict
        self.save_setting_files(self.config_path)

    def save_setting_files(self, path):
        """保存配置到本地文件"""
        try:
            with open(path, 'w') as file:
                json.dump(self.config_dict, file, indent=4)
            print(f"配置已成功保存到 {path}")
        except IOError as e:
            print(f"保存配置文件时发生错误：{e}")
        except Exception as e:
            print(f"保存配置文件时发生未知错误：{e}")

    @staticmethod
    def get_widget_center_pos(orgin):
        """获取控件的中心坐标"""
        center_pos = Pos(0, 0)
        if isinstance(orgin, QWidget):
            center_pos.x = orgin.pos().x() + orgin.width() / 2
            center_pos.y = orgin.pos().y() + orgin.height() / 2
        return center_pos

    def pic_process_by_info(self, img_info, way='search'):
        """图片识别_通过预读取的信息类"""
        path_list = img_info.path_list
        for path in path_list:
            pic = ag.locateOnScreen(path, confidence=0.9)
            if pic is not None:
                print(f"找到{path}")
                if way == 'click':
                    x, y = ag.center(pic)
                    ag.click(x, y, clicks=1, interval=1.0, button='left', duration=0.5, tween=ag.linear)
                    ag.moveTo(x + 20, y + 20, duration=0.8)

                return pic

    def press_key(self, msg, way='search'):
        ag.press(self.config_dict[msg])


class KeyboardListener(QThread):
    key_pressed = pyqtSignal(str)  # 定义一个新的信号用于发送按键事件

    def __init__(self):
        super().__init__()
        self.key_str = ''
        self.is_emit = False

    def run(self):

        def on_press(key):
            self.key_str = ''  # 手动清空一次键值，防止特殊键拼接时出错
            try:
                self.key_str = str(key.char)
            except AttributeError:
                # 如果是特殊按键，比如F1, Shift等
                temp = format(key)
                i = 0
                for char in temp:
                    i += 1
                    if i > 4:
                        self.key_str = self.key_str + char
            self.is_emit = True
            self.emit_key()

        def on_release(key):
            if key == Key.esc:
                # 停止监听，例如使用Esc键
                return False

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def emit_key(self):
        if self.is_emit:
            self.key_pressed.emit(self.key_str)  # 发射信号
            self.is_emit = False


class WorkerSignals(QObject):
    result = pyqtSignal(object)
    finish = pyqtSignal()
    error = pyqtSignal(tuple)


class Worker(QThread):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            self.signals.error.emit((type(e).__name__, str(e)))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finish.emit()


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Image_info:
    def __init__(self, name_list, path_list):
        self.name_list = name_list
        self.path_list = path_list
        # self.img_list = img_list
