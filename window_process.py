import time
import sys
import pygame
from pygame.locals import *
import logging
import ui
import cv2 as cv
from communicate import *


def window_process(show_msg_queue,back_queue,alive):
    window = ui.Window()
    show_image = cv.imread("./pic/background.jpeg")
    show_image = cv.transpose(show_image)
    pygame.event.set_allowed([MOUSEBUTTONDOWN,MOUSEMOTION,KEYUP,KEYDOWN])
    logger = logging.getLogger("show")
    logging.basicConfig(level=logging.DEBUG,
                        filename='./show.log',
                        filemode='w',
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        )
    while alive.value:
        t = time.time()
        if not show_msg_queue.empty():
            msg = show_msg_queue.get()
            show_image = msg.image
            window.debug = msg.debug
            window.show_battery = msg.battery
            window.show_hp = msg.hp
            window.show_heat = msg.heat
            if not msg.debug:
                show_image = cv.transpose(show_image)
        else:
            # msg = Msg(show_image, window.debug,battery=window.battery)
            time.sleep(0.005)
            logger.debug("MSG NONE")
        time.sleep(0.001)
        window.show(show_image)
        window.listener(back_queue,alive)
        logger.debug(f"show fps:{1/(time.time()-t)}")
    if not alive.value:
        back_queue.close()
        show_msg_queue.close()
        pygame.quit()

