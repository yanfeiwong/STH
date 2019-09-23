import subprocess,rospy,os,sys,time
from std_msgs.msg import String
from socket import *

Camera_Is_Running=0
Camera_Res=0
Camera_Kill=0

class Camera(object):
    def __init__(self):
        self.PID=''
        self.IsRunning=0
        self.NeedRes=0
        self.NeedKill=0
        self.C_RES_X=640
        self.C_RES_Y=480
        self.C_ISO=1200
        self.C_FRR=40
        self.C_hflip=True
        self.C_vflip=True
        self.C_host  = '192.168.3.17'
        self.C_port = 9922
        self.C_bufsize = 1024
    def Start(self):
        if Camera_Is_Running :
            self.
