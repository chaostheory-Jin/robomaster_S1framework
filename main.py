from mode_chooser import ModeChooser
import argparse
import pygame
import logging

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", default=False, help="debug mode", action="store_true")
parser.add_argument("-r", "--red", default=False, help="red mode", action="store_true")
parser.add_argument("-b", "--blue", default=False, help="blue mode", action="store_true")
parser.add_argument("-v", "--video", default=False, help="need video", action="store_true")

args = parser.parse_args()
logger = logging.getLogger()
if __name__ == '__main__':
    mode = ModeChooser('red')
    try:
        if args.video:
            mode.vd = True
        if args.red:
            mode.color = 'red'
        if args.blue:
            mode.color = 'blue'
        if args.debug:
            logger.setLevel(logging.DEBUG)
            mode.mode_set('debug')
        else:
            logger.setLevel(logging.INFO)
            mode.mode_set('race')
    except Exception as e:
        print("Someting Wrong:",e)
        pygame.quit()
        exit()
