import rospy,os
from std_msgs.msg import String
from socket import *

key="wangyan1840"
host = ''
port = 9921 
bufsize = 1024 
addr = (host,port)
udpServer = socket(AF_INET,SOCK_DGRAM) 
udpServer.bind(addr)

#######################Para_U_Power################################
PUP_Max_P=300.0
PUP_Power=0.0
PUP_Speed_D=0
PUP_res=0.5
PUP_running=0
PUP_need_restart=0
PUP_kill=0
########################Para_U_FPS#################################
PUF_res_X=1.0
PUF_res_Y=1.2
PUF_s1=27
PUF_s2=22
PUF_s1_m=1240
PUF_s2_m=1100
PUF_s1_max=2390
PUF_s1_min=500
PUF_s2_max=2200
PUF_s2_min=540
PUF_feq=60
PUF_port = 126
PUF_bufsize = 1024
PUF_running=0
PUF_need_restart=0
PUF_kill=0
########################Para_U_Cam#################################
C_RES_X=640
C_RES_Y=480
C_ISO=1200
C_FRR=40
C_hflip=True
C_vflip=True
C_host  = '192.168.3.17'
C_port = 9922
C_bufsize = 1024
C_running=0
C_need_restart=0
C_kill=0
##########################CMD_List##################################
CMD=["shutdown",
     "reboot",
     "power off",
     "power on",
     "fps off",
     "fps on",
     "camera off",
     "camera on",
     "set max power",
     "set power res",
     "set fps res x",
     "set fps res y",
     "set fps x min",
     "set fps x max",
     "set fps y min",
     "set fps y max",
     "set camera res x",
     "set camera res y",
     "set camera iso",
     "set camera fps",
     "set camera ip",
     "set camera port",
     "set power port",
     "set power port"
    ]
##########################Bas_Func##################################
def Get_Para(p):
    if p=="Power":
        p=[PUP_Max_P,
           PUP_Power,
           PUP_Speed_D,
           PUP_res,
           PUP_need_restart,
           PUP_kill]
    elif p=="FPS":
        p=[PUF_res_X,
           PUF_res_Y,
           PUF_s1,
           PUF_s2,
           PUF_s1_m,
           PUF_s2_m,
           PUF_s1_max,
           PUF_s1_min,
           PUF_s2_max,
           PUF_s2_min,
           PUF_feq,
           PUF_port,
           PUF_bufsize,
           PUF_running,
           PUF_need_restart,
           PUF_kill]
    elif p=="Camera":
        p=[C_RES_X,
           C_RES_Y,
           C_ISO,
           C_FRR,
           C_hflip,
           C_vflip,
           C_host,
           C_port,
           C_bufsize,
           C_running,
           C_need_restart,
           C_kill]
    else:
        p="non"
    return p
        
def Bot_CC():
    pub = rospy.Publisher('Bot_CC',String, queue_size=10)
    rospy.init_node('Bot',anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        data,addr = udpServer.recvfrom(bufsize) 
        data=data.decode()
        try:
            data=data.split(";")
            cc=CMD.index(data[0])
            if cc==0:
                os.system('echo'+key+'|sudo shutdown now')
            elif cc==1:
                os.system('echo'+key+'|sudo reboot now')
            elif 
        para_str = "para %s" % rospy.get_time()
        rospy.loginfo(para_str)
        pub.publish(para_str)
        #rate.sleep()
try:
    
    Bot_CC()
    #os.system('roscore')
except rospy.ROSInterruptException:
    pass

