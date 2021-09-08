from sys import exit
import pygame
from pygame.locals import *
from robomaster import *
import time
import logging
from Armor import armor
from basicrobot import BasicRobot

__all__ = ['S1Robot']


class S1Robot(BasicRobot):
    def __init__(self, name, debug, screen, color):
        """

        :param name: 机器人名字
        :param debug: 是否处于debug
        :param screen: 机器人显示的窗口
        :param color: 机器人的颜色
        """
        super(BasicRobot, self).__init__()
        self.color = color
        self.name = name
        self.debug = debug
        self.screen = screen                        # 机器人所在的窗口
        if not debug:
            self.s1 = robot.Robot()
            self.s1.initialize(conn_type='ap', proto_type='udp')
            self.s1.set_robot_mode(mode=robot.GIMBAL_LEAD)
            self.led = self.s1.led
            self.blaster = self.s1.blaster
            self.chassis = self.s1.chassis
            self.cam = self.s1.camera
            self.gimbal = self.s1.gimbal
            self.armor = self.s1.armor

            if color == 'red':
                self.led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
            if color == 'blue':
                self.led.set_led(comp=led.COMP_ALL, r=0, g=0, b=255, effect=led.EFFECT_ON)
            self.cam.start_video_stream(display=False)
            self.armor.sub_ir_event(callback=self.ir_hit_callback)
            self.s1.battery.sub_battery_info(freq=5,callback=self.battery_callback)
            self.armor.set_hit_sensitivity(sensitivity=10)
        else:
            self.pic = pygame.image.load('./pic/17.jpg')
            self.pos_x = 100
            self.pos_y = 100

        self.armor_detect = False
        self.action_state = True
        self.gimbal_action = ''

    def frame(self):
        image = self.cam.read_cv2_image()
        return image

    def move(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a):
                    self.speed_y -= 1
                elif event.key in (K_RIGHT, K_d):
                    self.speed_y += 1
                elif event.key in (K_UP, K_w):
                    self.speed_x += 1
                elif event.key in (K_DOWN, K_s):
                    self.speed_x -= 1
                elif event.key == K_ESCAPE:
                    self.__die()
                elif event.key == K_q:
                    self.armor_detect = True
                elif event.key == K_e:
                    self.armor_detect = False

            if event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    self.speed_y += 1
                elif event.key in (K_RIGHT, K_d):
                    self.speed_y -= 1
                elif event.key in (K_UP, K_w):
                    self.speed_x -= 1
                elif event.key in (K_DOWN, K_s):
                    self.speed_x += 1

            if event.type == MOUSEBUTTONDOWN:
                print("Fire")
                if not self.debug:
                    self.blaster.fire(blaster.INFRARED_FIRE,1)
                self.heat += self.unit_heat
                if self.heat > self.max_heat:
                    self.__hurt(flag='burn')
        if not self.debug:
            self.chassis.drive_speed(x=self.speed_x, y=self.speed_y, z=0, timeout=1)

    def aim(self,img):
        """
        :param img: 图片
        """
        if self.armor_detect:
            target = armor(img, debug=False,color=self.color)
            x,y = target
        else:
            x, y = pygame.mouse.get_pos()
        yaw = (x-360)/360 * 300
        pitch = (240-y)/240 * 25
        if not self.debug:
            if self.action_state:
                if -250 <= yaw <= 250 and (-25 <= pitch <= 30):
                    self.gimbal_action = self.gimbal.moveto(yaw=yaw,pitch=pitch,pitch_speed=500,yaw_speed=500)
                    self.action_state = self.gimbal_action.is_completed
            else:
                self.action_state = self.gimbal_action.is_completed
            logging.debug(f"action_state:{self.action_state}")

    def __hurt(self, flag:str):
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
            logging.info("Under attack")
        else:
            t_hit_hp = self.heat-self.max_heat
            if t_hit_hp < self.max_burn_hp:
                self.hp -= t_hit_hp
            else:
                self.hp -= self.max_burn_hp
            logging.info(f"Burn hp -{self.heat-self.max_heat}")

        if self.hp <= 0:
            self.hp = 0
            self.__die()

    def life(self):
        if self.hit_times:
            for idex in range(self.last_hit_times,self.hit_times):
                self.__hurt('hit')
                logging.info("under attack")
            self.last_hit_times = self.hit_times

    def __die(self):
        RIP = "GAME OVER"
        print(RIP)
        ft1_font = pygame.font.Font("./pic/font.ttf", 80)
        ft1_surf = ft1_font.render(RIP, 1, (0, 0, 255))
        self.screen.blit(ft1_surf, (100,150))
        pygame.display.flip()
        logging.info("die")
        time.sleep(1)
        if self.color == 'red':
            self.led.set_led(comp=led.COMP_ALL, r=0, g=0, b=255, effect=led.EFFECT_FLASH,freq=1)
        if self.color == 'blue':
            self.led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_FLASH,freq=1)
        pygame.quit()
        if not self.debug:
            self.cam.stop_video_stream()
            self.s1.close()
        if not self.debug:
            self.chassis.drive_speed(x=0, y=0, z=0, timeout=1)
        exit()

    def battery_callback(self,x):
        self.battery = x
        print(x,"battery")
        return self.battery

    def ir_hit_callback(self,x):
        self.hit_times = x
        print(x,"hit_times")
        return x
