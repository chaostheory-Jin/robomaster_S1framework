import time
import sys
import os
import pygame
from pygame.locals import *
import logging
import ui
import cv2 as cv
from communicate import *


def window_process(show_msg_queue,
                   back_queue,
                   alive,
                   lock):
    try:
        window = ui.Window()
        show_image = cv.imread("./pic/background.jpeg")
        show_image = cv.transpose(show_image)
        pygame.event.set_blocked([MOUSEMOTION])
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
                time.sleep(0.005)
                logger.debug("MSG NONE")
            window.listener(back_queue,alive)
            window.show(show_image,t)
    except Exception as e:
        logger.error(f"Error:{e}")
        lock.acquire()
        alive.value = False
        lock.release()
    finally:
        back_queue.close()
        show_msg_queue.close()
        pygame.quit()
        os._exit(1)

