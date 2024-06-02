import FishingTools


class Fishing():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Fishing, cls).__new__(cls)
        return cls._instance

    def __init__(self, widget):
        # super().__init__()
        self.widget = widget
        self.tool = FishingTools.Tool.get_instance()
        self.collect_img_list = self.get_img_list('collect')
        self.hold_img_list = self.get_img_list('hold')
        self.sale_img_list = self.get_img_list('sale')
        self.close_img_list = self.get_img_list('close')
        self.throw_img_list = self.get_img_list('throw')
        self.holding_img_list = self.get_img_list('holding')
        self.release_img_list = self.get_img_list('release')

    # 单例
    @staticmethod
    def get_instance(widget):
        if Fishing._instance is None:
            Fishing._instance = Fishing(widget)
        return Fishing._instance
    #
    # def fishing_start(self, state):
    #     print(f"{state},开始钓鱼")

    def get_img_list(self, img_name):
        print(f"[{img_name}]开始获取列表")
        img_list = self.tool.get_img_arr(self, img_name)
        return img_list
