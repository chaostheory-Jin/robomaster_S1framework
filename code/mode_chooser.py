import logging
import pygame
import sys
import main_process


class ModeChooser:

    def __init__(self,color:str):
        self.__colors =['red','blue']
        self.__modes = ['debug','race']
        self.color = color
        self.mode = 'race'
        self.video = False            #是否录像
        assert color in self.__colors,'color must be red or blue'

    def mode_set(self,mode:str,msg_queue,back_queue,alive):
        if self.mode in self.__modes:
            self.mode = mode
        else:
            logging.info("Mode Error,now mode:",self.mode)
        if self.mode == 'debug':
            main_process.mainprocess(self.video,self.color,
                                     debug=True,msg_queue=msg_queue,back_queue=back_queue,alive=alive)
        if self.mode == 'race':
            main_process.mainprocess(self.video,self.color,
                                     debug=False,msg_queue=msg_queue,back_queue=back_queue,alive=alive)

    def close(self,alive):
        alive.value = False
        pygame.quit()
        sys.exit()



