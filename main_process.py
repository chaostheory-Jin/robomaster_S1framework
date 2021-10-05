import time
import cv2 as cv
import logging

import sys
import os

from S1Robot import S1Robot
from communicate import Msg,BackMsg

def mainprocess(video:bool,
                color:str,
                debug:bool,
                msg_queue,
                back_queue,
                alive,lock):
    """

    :param video: bool类型，是否开启录屏，False为不开启
    :param color: 机器人颜色
    :return:
    """
    global video_src, read_video, write_video
    logger = logging.getLogger("control")
    if debug:
        logging.basicConfig(level=logging.DEBUG,
                            filename='./control.log',
                            filemode='w',
                            format=
                            '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                            )
        if color == 'red':
            video_src = './pic/s1blue.avi'
        if color == 'blue':
            video_src = './pic/s1red.avi'
        read_video = cv.VideoCapture(video_src)
    else:
        logging.basicConfig(level=logging.DEBUG,
                            filename='./control.log',
                            filemode='w',
                            format=
                            '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                            )
    try:
        s1 = S1Robot('S1', debug, color,alive)
        start_time = time.time()
        if video:
            fourcc = cv.VideoWriter_fourcc(*'XVID')
            write_video = cv.VideoWriter(f'./s1red.avi', fourcc, 30, (1280, 720), True)
        while alive.value:
            t = time.time()
            if not debug:
                img = s1.frame()
            else:
                ret, img = read_video.read()
                if not ret:
                    logging.debug("can`t read video or video have play over")
                    lock.acquire()
                    alive.value = False
                    lock.release()
                    continue
            if video:
                write_video.write(img)
            if not debug:
                s1.life()
            if not back_queue.empty():
                back_msg = back_queue.get()
                s1.move(back_msg)
                s1.aim(img,back_msg)
                logging.debug(f"back msg queue size:{back_queue.qsize()}")
            s1.cool()
            if not msg_queue.full():
                show_image = img
                if debug:
                    show_image = cv.transpose(show_image)
                massge = Msg(show_image,debug,s1.hp,s1.heat,s1.battery)
                msg_queue.put(massge)
            else:
                logging.debug("MSG FULL")
            logging.debug(f"control fps:{ 1/(time.time() - t)}")
            logging.info(f"{s1.__dict__}")
            if (time.time()-start_time)/1000 >= 5:
                lock.acquire()
                alive.value = False
                lock.release()
    except Exception as e:
        lock.acquire()
        alive.value = False
        lock.release()
        logging.error(f"{e}")
    os._exit(1)
