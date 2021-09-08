# 校内赛框架手册

## 1、框架说明

本框架为校内赛视觉使用框架，基于robomaster S1步兵。使用Python编写。

## 2、框架依赖

1、robomaser库

2、numpy库

3、OpenCV

4、pygame库

5、threading库

6、time库

安装：一般pip install就能解决

**目录结构：**

│  main.py
│  mode_chooser.py
│  project.txt
│  README.md
│  README.pdf
│  README.txt
│  s1process.py
│  
├─code
│  │  S1Robot.py
│  │  ui.py
│  │  
│  └─__pycache__
│          S1Robot.cpython-38.pyc
│          ui.cpython-38.pyc
│          
├─pic
│      17.jpg
│      A_PyGameMono-8.png
│      font.ttf
│      pygame.ico
│      pygame_icon.bmp
│      pygame_icon.tiff
│      pygame_logo.gif
│      pygame_powered.gif
│      pygame_small.gif
│      pygame_tiny.gif
│      s1blue.avi
│      s1red.avi
│      u13079_PyGameMono-8.png
│      
├─src

│  ……

└─vision
        Armor.py

## 3、使用说明

可读性：通过阅读main.py和armor.py两个文档协作者可以快速、高效地将视觉代码融入框架

**main.py**

通过终端开启，python main.py

后加参数：-d：debug模式,不添加-d即race比赛模式

​				    -r：选择红方

​                    -b：选择蓝方

​                    -v：是否开启录制

​					*debug模式下不支持录屏*

**键位说明**

通过wasd控制S1前进后退

通过Q开启自瞄，E关闭自瞄，Esc退出

**一旦按下Esc即退出，没有二次确认，慎重！**

**模式说明**

debug模式：

测试wasd控制为一个图片，控制图片运动

debug模式的视频为提前录制好的S1视角视频，可以正常开启自瞄

race模式：

正式比赛时的模式，可以选择是否录屏，不建议录屏，会影响代码运行速度。

wasd控制S1运动，底盘运动功率和速度为固定值无法调节，

**armor.py**

视觉代码部分，输入为img，debug，color

```
:param img：图片，debug时的输入img来源为视频，比赛时来源为相机
:param debug: bool类型，debug时会传入True，比赛时会传入False。
:param color: 颜色，str类型
:return: target是一个list，结构为[x,y]
```

## 历史版本

v1.0

S1框架完成
