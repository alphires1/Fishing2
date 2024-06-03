import timeit
import FishingTools
from pynput.keyboard import Key


class Fishing:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Fishing, cls).__new__(cls)
        return cls._instance

    def __init__(self, main_window):
        # super().__init__()
        # self.main_window = main_window
        self.operation_state = '停止运行'
        self.tool = FishingTools.Tool.get_instance()
        self.collect_img_info = self.get_img_info('collect')
        self.hold_img_info = self.get_img_info('hold')
        self.sale_img_info = self.get_img_info('sale')
        self.close_img_info = self.get_img_info('close')
        self.throw_img_info = self.get_img_info('throw')
        self.holding_img_info = self.get_img_info('holding')
        self.release_img_info = self.get_img_info('release')

    # 单例
    @staticmethod
    def get_instance(widget):
        if Fishing._instance is None:
            Fishing._instance = Fishing(widget)
        return Fishing._instance

    #
    def on_state_changed(self, new_state):
        self.operation_state = new_state
        print(self.operation_state)

    def fishing_start(self):
        start_time = timeit.default_timer()
        if self.operation_state == '开始运行':

            for pic in self.hold_img_info.name_list:
                if self.tool.pic_process_by_info(self.hold_img_info, 'click') is not None:
                    return "拉竿"
            _time = timeit.default_timer()
            print(f"拉竿耗时: {_time - start_time} seconds")
            for pic in self.throw_img_info.name_list:
                if self.tool.pic_process_by_info(self.throw_img_info) is not None:
                    self.tool.press_key('抛竿')
                    return "抛竿"

            for pic in self.collect_img_info.name_list:
                if self.tool.pic_process_by_info(self.collect_img_info) is not None:
                    self.tool.press_key('收藏')
                    return "收藏"
            for pic in self.sale_img_info.name_list:
                if self.tool.pic_process_by_info(self.sale_img_info) is not None:
                    self.tool.press_key('出售')
                    return "出售"
            for pic in self.holding_img_info.name_list:
                if pic is not None:
                    while self.tool.pic_process_by_info(self.holding_img_info) is not None:
                        self.tool.keyboard.press(Key.space)
                        for release in self.release_img_info.name_list:
                            if self.tool.pic_process_by_info(self.release_img_info) is not None:
                                self.tool.keyboard.release(Key.space)
            for pic in self.close_img_info.name_list:
                if self.tool.pic_process_by_info(self.close_img_info) is not None:
                    self.tool.press_key('esc', 'direct')
                    return "关闭遮挡"
            end_time = timeit.default_timer()
            print(f"主线程耗时: {end_time - start_time} seconds")
    def get_img_info(self, img_name):
        print(f"[{img_name}]开始获取列表")
        img_info = self.tool.get_img_info(img_name)

        return img_info
