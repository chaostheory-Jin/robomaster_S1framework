import argparse
import logging
import os
import sys
import multiprocessing as mp
import time

sys.path.append(os.path.abspath("./code"))
sys.path.append(os.path.abspath("./vision"))
sys.path.append(os.path.abspath("./basic"))
sys.path.append(os.path.abspath("./pic"))

from mode_chooser import ModeChooser
from window_process import window_process


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", default=False, help="video debug mode", action="store_true")
parser.add_argument("-r", "--red", default=False, help="red mode", action="store_true")
parser.add_argument("-b", "--blue", default=False, help="blue mode", action="store_true")
parser.add_argument("-v", "--video", default=False, help="need video", action="store_true")
args = parser.parse_args()
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    mode = ModeChooser('red')
    msg_queue = mp.Queue()
    back_queue = mp.Queue()
    alive = mp.Value('b',True)
    lock = mp.Lock()
    show_process = mp.Process(target=window_process, args=(msg_queue,back_queue,alive,lock),name="consumer")
    show_process.daemon = True
    show_process.start()
    if args.video:
        mode.video = True
    if args.red:
        mode.color = 'red'
    if args.blue:
        mode.color = 'blue'
    if args.debug:
        logger.setLevel(logging.DEBUG)
        contr_process = mp.Process(target=mode.mode_set,args=("debug",msg_queue,back_queue,alive,lock),name="producer")
        contr_process.daemon = True
        contr_process.start()
        contr_process.join()
    else:
        contr_process = mp.Process(target=mode.mode_set,args=("race",msg_queue,back_queue,alive,lock),name="producer")
        contr_process.daemon = True
        contr_process.start()
        contr_process.join()

