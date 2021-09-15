from msg import BasicMsg


class Msg(BasicMsg):
    def __init__(self,image,debug=False,hp=600,heat=0,battery=100):
        super(Msg, self).__init__()
        self.image = image
        self.hp = hp
        self.heat = heat
        self.battery = battery
        self.debug = debug


class BackMsg(BasicMsg):
    def __init__(self,speed_x=0,speed_y=0,
                 mouse_pos_x=640,mouse_pos_y=360,
                 go_out=False,armor_detect=False,fire=False):
        super(BackMsg, self).__init__(speed_x,speed_y)
        self.armor_detect = armor_detect
        self.go_out = go_out
        self.fire = fire
        self.mouse_move_x = mouse_pos_x
        self.mouse_move_y = mouse_pos_y
