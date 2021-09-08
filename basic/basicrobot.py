class BasicRobot:
    def __init__(self):
        self.armor_detect = False
        self.action_state = True

        self.hp = 1200                               # 机器人血量
        self.heat = 0                                # 机器人热量
        self.battery = 100
        self.hit_times = 0
        self.last_hit_times = 0

        self.max_heat = 150
        self.hit_hp = 15
        self.unit_heat = 25
        self.max_burn_hp = 25

        self.speed_x = 0
        self.speed_y = 0

    def life(self):
        NotImplemented

    def move(self):
        NotImplemented

    def rotate(self):
        NotImplemented
