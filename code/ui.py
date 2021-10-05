import logging
import time

import cv2 as cv
import pygame
from pygame.locals import *

from communicate import *

__all__ = ['Window']

class Window:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), flags=pygame.DOUBLEBUF)
        self.speed_x = 0
        self.speed_y = 0
        self.last_mouse_position_x = 640
        self.last_mouse_position_y = 360
        self.flag = 1
        self.debug = False
        self.show_battery = 100
        self.show_hp = 600
        self.show_heat = 0
        self.armor_detect = False
        pygame.display.set_caption("SRM校内赛")
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def show(self,img,t):
        show_image = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        pygame.surfarray.blit_array(self.screen, show_image)
        ft1_font = pygame.font.Font("./pic/font2.ttf", 30)
        hp_surf = ft1_font.render(f"HP:{self.show_hp}(Max:600)", 1, (10, 180, 10))
        heat_surf = ft1_font.render(f"CAL:{self.show_heat}(Max:150)", 1, (160, 20, 10))
        fps = ft1_font.render(f"show fps:{int(1/(time.time()-t))}",1, (0, 100, 255))
        self.screen.blit(hp_surf, (100, 50))
        self.screen.blit(heat_surf, (100, 100))
        self.screen.blit(fps,(100,150))
        if not self.debug:
            battery_surf = ft1_font.render(f"BATTERY POWER:{self.show_battery}", 1,(10, 255, 10))
            self.screen.blit(battery_surf, (800, 80))
        pygame.display.flip()

    def listener(self,back_queue,alive):
        back_msg = BackMsg()
        for event in pygame.event.get():
            if event.type == QUIT:
                back_msg.go_out = True
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
                    RIP = "GAME OVER"
                    logging.info(RIP)
                    ft1_font = pygame.font.Font("./pic/font.ttf", 80)
                    ft1_surf = ft1_font.render(RIP, 1, (0, 0, 255))
                    self.screen.blit(ft1_surf, (100,150))
                    pygame.display.flip()
                    back_msg.go_out = True
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
                back_msg.fire = True

        x,y = pygame.mouse.get_pos()
        back_msg.mouse_move_x = 640 - x
        back_msg.mouse_move_y = 360 - y
        pygame.mouse.set_pos(640,360)

        back_msg.speed_y = self.speed_y
        back_msg.speed_x = self.speed_x
        back_msg.armor_detect = self.armor_detect
        self.send(back_queue, back_msg)
        back_queue_size = back_queue.qsize()
        if back_msg.go_out:
            alive.value = False

    def send(self,back_queue,back_msg):
        if not back_queue.full():
            back_queue.put(back_msg)
        else:
            if back_msg.fire:
                _ = back_queue.get()
                back_queue.put(back_msg)
            print("BACK FULL")
