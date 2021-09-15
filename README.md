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

或者使用目录下的requirements安装。

使用方法：进入到框架主目录下，打开终端，在终端内使用命令：**pip install -r requirements.txt**

**目录结构：**
│  control.log
│  main.py
│  main_process.py
│  README.md
│  README.pdf
│  README.txt
│  requirements.txt
│  show.log
│  tree.txt
│  window_process.py
│  
├─.idea
│  │  .gitignore
│  │  misc.xml
│  │  modules.xml
│  │  S1framework.iml
│  │  vcs.xml
│  │  workspace.xml
│  │  
│  └─inspectionProfiles
│          profiles_settings.xml
│          Project_Default.xml
│          
├─basic
│  │  basicrobot.py
│  │  msg.py
│  │  
│  └─__pycache__
│          basicrobot.cpython-38.pyc
│          msg.cpython-38.pyc
│          
├─code
│  │  communicate.py
│  │  mode_chooser.py
│  │  S1Robot.py
│  │  ui.py
│  │  
│  └─__pycache__
│          communicate.cpython-38.pyc
│          mode_chooser.cpython-38.pyc
│          S1Robot.cpython-38.pyc
│          ui.cpython-38.pyc
│          
├─pic
│      background.jpeg
│      font.ttf
│      font2.ttf
│      s1blue.avi
│      s1red.avi
│      
├─vision
│  │  Armor.py
│  │  
│  └─__pycache__
│          Armor.cpython-38.pyc
│          
└─__pycache__
        main_process.cpython-38.pyc
        window_process.cpython-38.pyc

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

wasd控制S1运动，底盘运动功率和速度为固定值无法调节。

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

v1.3

提高了帧率，解决了一系列bug，完善了对战模式功能

v1.4

代码结构改为多进程形式，优化了代码框架
