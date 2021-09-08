import os
import sys
import pygame
import time
import cv2 as cv
import logging

sys.path.append(os.path.abspath("./code"))
sys.path.append(os.path.abspath("./vision"))
sys.path.append(os.path.abspath("./src"))
sys.path.append(os.path.abspath("./basic"))

from S1Robot import S1Robot
import ui


logging.basicConfig(level=logging.DEBUG)

def mainprocess(vd:bool, color:str,debug:bool):
    """
    主线程
    :param vd: bool类型，是否开启录屏，0为不开启
    :param color: 机器人颜色
    :return:
    """
    screen = ui.init()
    if debug:
        robot_image = '../pic/17.jpg'
        if color == 'red':
            video_src = './pic/s1blue.avi'
        if color == 'blue':
            video_src = './pic/s1red.avi'
        video = cv.VideoCapture(video_src)

    s1 = S1Robot('S1', debug, screen, color)
    if vd:
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        t = time.gmtime()
        video = cv.VideoWriter(f'./{time.strftime("%Y-%m-%d %H:%M:%S", t)}s1red.avi', fourcc, 30, (1280, 720), True)
    now = time.time()
    while True:
        if not debug:
            img = s1.frame()
        else:
            ret, img = video.read()
            if not ret:
                logging.debug("can`t read video or video have play over")
                exit()
        if vd:
            video.write(img)
        if not debug:
            s1.life()

        ui.window(img,s1,screen)
        s1.move()
        s1.aim(img)
        pygame.display.flip()

        time_gap = time.time()-now
        if 0.95 < time_gap < 1.05:
            now = time.time()
            if s1.heat > s1.unit_heat:
                s1.heat -= 15
            elif s1.heat > 0:
                s1.heat = 0

        if s1.hp <= 0:
            pygame.quit()
            if vd:
                video.release()
            if not debug:
                s1.cam.stop_video_stream()
                s1.s1.close()
            break
