import subprocess,sys,argparse,rospy,os,ast
from socket import *

parser = argparse.ArgumentParser()

parser.add_argument("--type",default='def')

args = parser.parse_args()



BCC_F="Bot_CC_V2"
BCC_PID=''
BCC_Is_Running=0
BCC_Res=0
BCC_Kill=0

Camera_F="p2s_V2.py"
Camera_PID=''
Camera_Is_Running=0
Camera_Res=0
Camera_Kill=0

Power_F="U_Power_V2.py"
Power_PID=''
Power_Is_Running=0
Power_Res=0
Power_Kill=0

FPS_F="U_FPS_V2.py"
FPS_PID=''
FPS_Is_Running=0
FPS_Res=0
FPS_Kill=0

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
    def Para_Update_out(self):
        global Camera_PID,Camera_Is_Running,Camera_Res,Camera_Kill
        Camera_PID=self.PID
        Camera_Is_Running=self.IsRunning
        Camera_Res=self.NeedRes
        Camera_Kill=self.NeedKill
    def Update(self,data):
        d=ast.literal_eval(data)
        self.C_RES_X=d[0]
        self.C_RES_Y=d[1]
        self.C_ISO=d[2]
        self.C_FRR=d[3]
        self.C_hflip=d[4]
        self.C_vflip=d[5]
        self.C_host=d[6]
        self.C_port=d[7]
        self.C_bufsize=d[8]
        self.IsRunning=d[9]
        self.NeedRes=d[10]
        self.NeedKill=d[11]
    def Start(self):
        if Camera_Is_Running :
            self.Kill()
            print("Camera is running, will restart")
            self.Start()
        else:
            argument =  "  --C_RES_X  "+str(self.C_RES_X)\
                       +"  --C_RES_Y  "+str(self.C_RES_Y)\
                       +"  --C_ISO  "+str(self.C_ISO)\
                       +"  --C_FRR  "+str(self.C_FRR)\
                       +"  --C_hflip  "+str(self.C_hflip)\
                       +"  --C_vflip  "+str(self.C_vflip)\
                       +"  --C_host  "+self.C_host\
                       +"  --C_port  "+str(self.C_port)
            
            self.proc = subprocess.Popen(['python3', Camera_F , argument], shell=True)
            self.PID = self.proc.pid
            self.IsRunning=1
            self.Para_Update_out()
            print(Camera_PID)
    def Kill(self):
        try:
            self.proc.terminate()
            self.PID=''
            self.NeedKill=0
            self.IsRunning=0
            self.Para_Update_out()
        except:
            print("Erro : Failed to kill Camera. Pid",+str(self.PID)+sys.exc_info()[0])
            raise
        
class Power(object):
    def __init__(self):
        self.PUP_Max_P=300.0
        self.PUP_Power=0.0
        self.PUP_Speed_D=0
        self.PUP_res=0.5
        self.PUP_running=0
        self.PUP_need_restart=0
        self.PUP_kill=0
        self.PUP_port = 124
    def Para_Update_out(self):
        global Power_PID,Power_Is_Running,Power_Res,Power_Kill
        Power_PID=self.PID
        Power_Is_Running=self.PUP_IsRunning
        Power_Res=self.PUP_need_restart
        Power_Kill=self.PUP_kill
    def Update(self,data):
        d=ast.literal_eval(data)
        self.PUP_Max_P=d[0]
        self.PUP_Power=d[1]
        self.PUP_Speed_D=d[2]
        self.PUP_res=d[3]
        self.PUP_need_restart=d[4]
        self.PUP_kill=d[5]
    def Start(self):
        if Power_Is_Running :
            self.Kill()
            print("Power is running, will restart")
            self.Start()
        else:
            argument =  "  --PUP_Max_P  "+str(self.PUP_Max_P)\
                       +"  --PUP_Power  "+str(self.PUP_Power)\
                       +"  --PUP_Speed_D  "+str(self.PUP_Speed_D)\
                       +"  --PUP_res  "+str(self.PUP_res)\
                       +"  --PUP_port  "+str(self.PUP_port)\
            
            self.proc = subprocess.Popen(['python3', Power_F , argument], shell=True)
            self.PID = self.proc.pid
            self.PUP_IsRunning=1
            self.Para_Update_out()
            print(Power_PID)
    def Kill(self):
        try:
            self.proc.terminate()
            self.PID=''
            self.PUP_kill=0
            self.PUP_IsRunning=0
            self.Para_Update_out()
        except:
            print("Erro : Failed to kill Power. Pid",+str(self.PID)+sys.exc_info()[0])
            raise
        
class FPS(object):
    def __init__(self):
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
    def Para_Update_out(self):
        global FPS_PID,FPS_Is_Running,FPS_Res,FPS_Kill
        FPS_PID=self.PID
        FPS_Is_Running=self.IsRunning
        FPS_Res=self.NeedRes
        FPS_Kill=self.NeedKill
    def Start(self):
        if Power_Is_Running :
            self.Kill()
            print("FPS is running, will restart")
            self.Start()
        else:
            argument =  "  --PUF_res_X  "+str(self.PUF_res_X)\
                       +"  --PUF_res_Y  "+str(self.PUF_res_Y)\
                       +"  --PUF_port  "+str(self.PUF_port)\
            
            self.proc = subprocess.Popen(['python3', FPS_F , argument], shell=True)
            self.PID = self.proc.pid
            self.IsRunning=1
            self.Para_Update_out()
            print(FPS_PID)
    def Kill(self):
        try:
            self.proc.terminate()
            self.PID=''
            self.NeedKill=0
            self.IsRunning=0
            self.Para_Update_out()
        except:
            print("Erro : Failed to kill FPS. Pid",+str(self.PID)+sys.exc_info()[0])
            raise
        
def callback(data):
    data=data.data.split(';;')
    try:
        if data[0]=="c":
            camera.Update(data[1])
        elif data[0]=="p":
            bpower.Update(data[1])
        elif data[1]=="f":
            Fpower.Update(data[1])
    except:
        print("Failed to pudate paras : "+ str(data))
            
def listener():
    rospy.init_node('MPM', anonymous=True)
    rospy.Subscriber('Bot_CC', String, callback)
    rospy.spin()

def main():
    try:
        if args.type=="def":
            camera=Camera()
            camera.Start()
            bpower=Power()
            bpower.Start()
            bfps=FPS()
            bfps.Start()
        elif args.type[0]=="1":
            camera=Camera()
            camera.Start()
        elif args.type[1]=="1":
            bpower=Power()
            bpower.Start()
        elif args.type[2]=="1":
            bfps=FPS()
            bfps.Start()
        else:
            pass
    except:
        U_Sender("Erro :",sys.exc_info()[0])
        raise
    
    listener() 
    
        
camera.Kill()
bpower.Kill()
bfps.Kill()
