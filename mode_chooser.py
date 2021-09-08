import s1process as ps
import time


class ModeChooser:

    def __init__(self,color:str):
        self.__colors =['red','blue']
        self.__modes = ['debug','race']
        self.color = color
        self.mode = 'race'
        self.vd = False
        assert color in self.__colors,'color must be red or blue'

    def mode_set(self,mode:str):
        if self.mode in self.__modes:
            self.mode = mode
        else:
            print("Mode Error,now mode:",self.mode)
            time.sleep(5)
        if self.mode == 'debug':
            ps.mainprocess(self.vd,self.color,debug=True)
        if self.mode == 'race':
            ps.mainprocess(self.vd,self.color,debug=False)




