import rospy,os,sys
from std_msgs.msg import String
from socket import *
from Start_ROS import *
############################Def_Para###############################
#Bas
key="some key here"
Subp_Started=0
Subp_Runing=0
Subp_Kill=0
#U_Rec
host = ''
port = 9921 
bufsize = 1024 
addr = (host,port)
#U_Sed
S_host  = '192.168.31.119'
S_port = 9999
S_bufsize = 1024
r_addr = (host,port)

udpServer = socket(AF_INET,SOCK_DGRAM)
udpClient.sendto(data,addr)
udpServer.bind(addr)

class Paras(object):
    def __init__(self):
#######################Para_U_Power################################
        self.PUP_Max_P=300.0
        self.PUP_Power=0.0
        self.PUP_Speed_D=0
        self.PUP_res=0.5
        self.PUP_running=0
        self.PUP_need_restart=0
        self.PUP_kill=0
        self.PUP_port = 124
########################Para_U_FPS#################################
        self.PUF_res_X=1.0
        self.PUF_res_Y=1.2
        self.PUF_s1=27
        self.PUF_s2=22
        self.PUF_s1_m=1240
        self.PUF_s2_m=1100
        self.PUF_s1_max=2390
        self.PUF_s1_min=500
        self.PUF_s2_max=2200
        self.PUF_s2_min=540
        self.PUF_feq=60
        self.PUF_port = 126
        self.PUF_bufsize = 1024
        self.PUF_running=0
        self.PUF_need_restart=0
        self.PUF_kill=0
########################Para_U_Cam#################################
        self.C_RES_X=640
        self.C_RES_Y=480
        self.C_ISO=1200
        self.C_FRR=40
        self.C_hflip=True
        self.C_vflip=True
        self.C_host  = '192.168.3.17'
        self.C_port = 9922
        self.C_bufsize = 1024
        self.C_running=0
        self.C_need_restart=0
        self.C_kill=0

    def Get_Para(self,p):
        if p=="Power":
            p=[self.PUP_Max_P,
               self.PUP_Power,
               self.PUP_Speed_D,
               self.PUP_res,
               self.PUP_need_restart,
               self.PUP_kill]
        elif p=="FPS":
            p=[self.PUF_res_X,
               self.PUF_res_Y,
               self.PUF_s1,
               self.PUF_s2,
               self.PUF_s1_m,
               self.PUF_s2_m,
               self.PUF_s1_max,
               self.PUF_s1_min,
               self.PUF_s2_max,
               self.PUF_s2_min,
               self.PUF_feq,
               self.PUF_port,
               self.PUF_bufsize,
               self.PUF_running,
               self.PUF_need_restart,
               self.PUF_kill]
        elif p=="Camera":
            p=[self.C_RES_X,
               self.C_RES_Y,
               self.C_ISO,
               self.C_FRR,
               self.C_hflip,
               self.C_vflip,
               self.C_host,
               self.C_port,
               self.C_bufsize,
               self.C_running,
               self.C_need_restart,
               self.C_kill]
        else:
            p="non"
        return p
    
##########################CMD_List##################################
CMD=["shutdown",#0
     "reboot",
     "power off",
     "power on",
     "fps off",
     "fps on",#5
     "camera off",
     "camera on",
     "set max power",
     "set power res",
     "set fps res x",#10
     "set fps res y",
     "set fps x min",
     "set fps x max",
     "set fps y min",
     "set fps y max",#15
     "set camera res x",
     "set camera res y",
     "set camera iso",
     "set camera fps",
     "set camera ip",#20
     "set camera port",
     "set power port",
     "set fps port"
    ]
##########################Bas_Func##################################
def U_Sender(ustr,s_addr=r_addr,show_text=1):
    try:
        data = ustr.encode()
        udpClient.sendto(data,s_addr)
        if show_text==1:
            print('send "'+ustr+' " to  '+str(s_addr))
    except e:
        print("Erro : U_Sender",sys.exc_info()[0])
        raise


        
def Bot_CC():
    Bot_Para=Paras()
    pub = rospy.Publisher('Bot_CC',String, queue_size=15)
    rospy.init_node('Bot',anonymous=True)
    U_Sender("Control center Online")
    #rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        data,addr = udpServer.recvfrom(bufsize) 
        data=data.decode()
        try:
            if data=="exit":
                break
            data=data.split(";")
            cc=CMD.index(data[0])
            if cc==0:
                roscore.terminate()
                os.system('echo'+key+'|sudo shutdown now')
            elif cc==1:
                roscore.terminate()
                os.system('echo'+key+'|sudo reboot now')
            elif cc==2:
                Bot_Para.PUP_running=0
                Bot_Para.PUP_need_restart=0
                Bot_Para.PUP_kill=1
                para_str = "p;;"+Bot_Para.Get_Para("Power")
                rospy.loginfo(para_str)
                pub.publish(para_str)
            elif cc==3:
                Bot_Para.PUP_running=1
                Bot_Para.PUP_need_restart=0
                Bot_Para.PUP_kill=0
                para_str = "p;;"+Bot_Para.Get_Para("Power")
                rospy.loginfo(para_str)
                pub.publish(para_str)
            elif cc==4:
                Bot_Para.PUF_running=0
                Bot_Para.PUF_need_restart=0
                Bot_Para.PUF_kill=1
                para_str = "f;;"+Bot_Para.Get_Para("FPS")
                rospy.loginfo(para_str)
                pub.publish(para_str)
            elif cc==5:
                Bot_Para.PUF_running=1
                Bot_Para.PUF_need_restart=0
                Bot_Para.PUF_kill=0
                para_str = "f;;"+Bot_Para.Get_Para("FPS")
                rospy.loginfo(para_str)
                pub.publish(para_str)
            elif cc==6:
                Bot_Para.C_running=0
                Bot_Para.C_need_restart=0
                Bot_Para.C_kill=1
                para_str = "c;;"+Bot_Para.Get_Para("Camera")
                rospy.loginfo(para_str)
                pub.publish(para_str)
            elif cc==7:
                Bot_Para.C_running=1
                Bot_Para.C_need_restart=0
                Bot_Para.C_kill=0
                para_str = "c;;"+Bot_Para.Get_Para("Camera")
                rospy.loginfo(para_str)
                pub.publish(para_str)
            elif cc==16:
                Bot_Para.C_RES_X=int(data[1])
                para_str = "c;;"+Bot_Para.Get_Para("Camera")
                rospy.loginfo(para_str)
                pub.publish(para_str)
                Bot_Para.C_need_restart=0
            elif cc==17:
                Bot_Para.C_RES_Y=int(data[1])
                Bot_Para.C_need_restart=1
                para_str = "c;;"+Bot_Para.Get_Para("Camera")
                rospy.loginfo(para_str)
                pub.publish(para_str)
                Bot_Para.C_need_restart=0
            elif cc==18:
                Bot_Para.C_ISO=int(data[1])
                Bot_Para.C_need_restart=1
                para_str = "c;;"+Bot_Para.Get_Para("Camera")
                rospy.loginfo(para_str)
                pub.publish(para_str)
                Bot_Para.C_need_restart=0
            elif cc==19:
                Bot_Para.C_FPS=int(data[1])
                Bot_Para.C_need_restart=1
                para_str = "c;;"+Bot_Para.Get_Para("Camera")
                rospy.loginfo(para_str)
                pub.publish(para_str)
                Bot_Para.C_need_restart=0
            elif cc==20:
                Bot_Para.C_host=data[1]
                Bot_Para.C_need_restart=1
                para_str = "c;;"+Bot_Para.Get_Para("Camera")
                rospy.loginfo(para_str)
                pub.publish(para_str)
                Bot_Para.C_need_restart=0
            elif cc==21:
                Bot_Para.C_port=int(data[1])
                Bot_Para.C_need_restart=1
                para_str = "c;;"+Bot_Para.Get_Para("Camera")
                rospy.loginfo(para_str)
                pub.publish(para_str)
                Bot_Para.C_need_restart=0
            elif cc==22:
                Bot_Para.PUP_port=int(data[1])
                Bot_Para.PUP_need_restart=1
                para_str = "p;;"+Bot_Para.Get_Para("Power")
                rospy.loginfo(para_str)
                pub.publish(para_str)
                Bot_Para.PUP_need_restart=0
            elif cc==23:
                Bot_Para.PUF_port=int(data[1])
                Bot_Para.PUF_need_restart=1
                para_str = "f;;"+Bot_Para.Get_Para("Power")
                rospy.loginfo(para_str)
                pub.publish(para_str)
                Bot_Para.PUF_need_restart=0
        except:
            pass

if __name__ == '__main__':
    try:
        roscore = Roscore()
        roscore.run()
        time.sleep(3)
        Bot_CC()
        roscore.terminate()
        U_Sender("Control center OUT")
        exit(0)
    except:
        U_Sender("Erro : Control center OUT！",sys.exc_info()[0])
        raise
    exit(0)

