import cv2 as cv
import time


def armor(img, debug: bool,color:str) -> list:
    """
    该函数为视觉处理函数。
    :param img: 图片，debug时的输入img来源为视频，比赛时来源为相机
    :param debug: bool类型，debug时会传入True，比赛时会传入False。
    :param color: 颜色，str类型
    :return: target是一个list，结构为[x,y]
    """
    img_debug = img.copy()
    target = [640, 360]
    print("AIMING")
    """
    ###########################
        校内赛视觉代码区域
    ###########################
    """
    # cv.imshow('image',img)
    return target
