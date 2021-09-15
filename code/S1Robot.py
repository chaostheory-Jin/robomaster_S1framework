import sys
import pygame
from pygame.locals import *
from robomaster import *
import time
import logging
from Armor import armor
from basicrobot import BasicRobot

__all__ = ['S1Robot']

IMAGE_POSITION_X = 100
IMAGE_POSITION_Y = 100
SCREEN_SIZE_X = 1280
SCREEN_SIZE_Y = 720
GIMBAL_SPEED_YAW = 100
GIMBAL_SPEED_PITCH = 100


class S1Robot(BasicRobot):
    def __init__(self, name, debug, color,alive):
        """

        :param name: 机器人名字
        :param debug: 是否处于debug
        :param color: 机器人的颜色
        """
        super().__init__()
        self.color = color
        self.name = name
        self.debug = debug
        if not debug:
            self.s1 = robot.Robot()
            self.s1.initialize(conn_type='ap', proto_type='udp')
            self.led = self.s1.led
            self.blaster = self.s1.blaster
            self.chassis = self.s1.chassis
            self.cam = self.s1.camera
            self.gimbal = self.s1.gimbal
            self.armor = self.s1.armor

            logging.debug(self.s1.set_robot_mode(mode=robot.GIMBAL_LEAD))
            if color == 'red':
                self.led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
            if color == 'blue':
                self.led.set_led(comp=led.COMP_ALL, r=0, g=0, b=255, effect=led.EFFECT_ON)

            self.cam.start_video_stream(display=False)
            self.armor.sub_ir_event(callback=self.ir_hit_callback)
            self.s1.battery.sub_battery_info(freq=5,callback=self.battery_callback)
            self.gimbal.sub_angle(callback=self.angle_callback)
            self.armor.set_hit_sensitivity(sensitivity=10)

        self.armor_detect = False
        self.action_state = True
        self.alive = alive
        self.gimbal_action = ''
        self.last_cool_time = time.time()

    def frame(self):
        image = self.cam.read_cv2_image()
        return image

    def move(self,back_msg):
        if back_msg.go_out:
            self.__die()
        if not self.debug:
            self.chassis.drive_speed(x=back_msg.speed_x, y=back_msg.speed_y, z=0, timeout=1)
    def aim(self,img,back_msg):
        """
        :param backmsg: 返回msg
        :param img: 图片
        """
        if self.armor_detect:
            target = armor(img, debug=False,color=self.color)
            x,y = target
            yaw = (x - SCREEN_SIZE_X/2) / SCREEN_SIZE_X * 125
            pitch = (SCREEN_SIZE_Y/2 - y) / SCREEN_SIZE_Y * 20
        else:
            mouse_move_x = back_msg.mouse_move_x
            mouse_move_y = back_msg.mouse_move_y

            yaw = mouse_move_x/SCREEN_SIZE_X * 120
            pitch = mouse_move_y/SCREEN_SIZE_Y * 20
        if not self.debug:
            if self.action_state:
                if 50>abs(yaw)>=3 or 10>abs(pitch)>3:
                    self.gimbal_action = self.gimbal.move(yaw=yaw,pitch=pitch,
                                                            pitch_speed=GIMBAL_SPEED_PITCH,yaw_speed=GIMBAL_SPEED_YAW)
                    self.action_state = self.gimbal_action.is_completed
            else:
                self.action_state = self.gimbal_action.is_completed
        if back_msg.fire:
            if not self.debug:
                self.blaster.set_led(200)
                self.blaster.fire(blaster.INFRARED_FIRE,1)
            self.heat += self.fire_heat
            if self.heat > self.max_heat:
                self.__bleed(flag='burn')
        logging.debug(f"x,y{yaw,pitch}")

    def __bleed(self, flag:str):
        """

        :param flag: flag='burn' 表示自己热量超限受伤,flag='hit' 表示挨打受伤
        :return:
        """
        if flag == 'hit':
            self.hp -= self.hit_hp
            if not self.debug:
                if self.color == 'red':
                    self.led.set_led(comp=led.COMP_ALL, r=0, g=0, b=255, effect=led.EFFECT_OFF)
                    time.sleep(0.03)
                    self.led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
                if self.color == 'blue':
                    self.led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_FLASH,freq=1)
                    time.sleep(0.03)
                    self.led.set_led(comp=led.COMP_ALL, r=0, g=0, b=255, effect=led.EFFECT_ON)

        else:
            t_burn_hp = self.heat-self.max_heat
            if t_burn_hp < self.max_burn_hp:
                self.hp -= t_burn_hp
                logging.info(f"Burn hp -{self.heat - self.max_heat}")
            else:
                self.hp -= self.max_burn_hp
                logging.info(f"Burn hp -{self.max_burn_hp}")

        if self.hp <= 0:
            self.hp = 0
            self.__die()

    def life(self):
        if self.hit_times - self.last_hit_times:
            for idex in range(self.last_hit_times,self.hit_times):
                self.__bleed('hit')
                logging.info("Under attack")
            self.last_hit_times = self.hit_times

    def __die(self):
        self.hp = 0
        if not self.debug:
            self.chassis.drive_speed(x=0, y=0, z=0, timeout=1)
            if self.color == 'red':
                self.led.set_led(comp=led.COMP_ALL, r=0, g=0, b=255, effect=led.EFFECT_FLASH,freq=1)
            if self.color == 'blue':
                self.led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_FLASH,freq=1)
        if not self.debug:
            self.cam.stop_video_stream()
            self.s1.close()
        self.alive.value = False

    def cool(self):
        time_gap = time.time() - self.last_cool_time
        if 0.95 < time_gap < 1.05:
            self.last_cool_time = time.time()
            if self.heat > self.cool_heat:
                self.heat -= self.cool_heat
            elif self.heat > 0:
                self.heat = 0

    def battery_callback(self,x):
        self.battery = x
        logging.debug(f"battery{x}")
        return self.battery

    def ir_hit_callback(self,x):
        self.hit_times = x
        logging.debug(f"hit_times{x}")
        return x

    def angle_callback(self,x1):
        self.angle = x1
        # logging.debug(x1,"S1 gimbal angle")
        return x1
