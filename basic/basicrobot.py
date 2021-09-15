class BasicRobot:
    def __init__(self):
        self.armor_detect = False
        self.action_state = True

        self.hp = 600                               # 机器人血量
        self.heat = 0                                # 机器人热量
        self.battery = 100
        self.hit_times = 0
        self.last_hit_times = 0
        self.last_mouse_position_x = 720
        self.last_mouse_position_y = 360
        self.current_mouse_positon_x = 720
        self.current_mouse_positon_y = 360

        self.max_heat = 150
        self.hit_hp = 15
        self.fire_heat = 25
        self.cool_heat = 15
        self.max_burn_hp = 35
        self.angle = 0

        self.speed_x = 0
        self.speed_y = 0

    def life(self):
        NotImplemented

    def move(self):
        NotImplemented

    def rotate(self):
        NotImplemented
