import pigpio,os,time,sys,argparse
from socket import *

parser = argparse.ArgumentParser()

parser.add_argument("--PUF_res_X",default=1.0, type=float)
parser.add_argument("--PUF_res_Y",default=1.2, type=float)
parser.add_argument("--PUF_port",default=126, type=int)

args = parser.parse_args()

try:
    os.system("sudo pigpiod")
    tim.sleep(2)
except:
    pass

res_X=args.PUF_res_X
res_Y=args.PUF_res_Y
s1=27
s2=22
s1_m=1240
s2_m=1100
s1_max=2390
s1_min=500
s2_max=2200
s2_min=540
feq=60
ps_1=s1_m
ps_2=s2_m
pi = pigpio.pi()
pi.set_PWM_frequency(s1,feq)
pi.set_PWM_frequency(s2,feq)
pi.set_servo_pulsewidth(s1,s1_m)
pi.set_servo_pulsewidth(s2,s2_m)


def stop():
    pi.set_servo_pulsewidth(s1,0)
    pi.set_servo_pulsewidth(s2,0)
def mid():
    global ps_1,ps_2
    ps_1=s1_m
    ps_2=s2_m
    pi.set_servo_pulsewidth(s1,s1_m)
    pi.set_servo_pulsewidth(s2,s2_m)
def set_p(s,p,sm,smax):
    if p>=sm and p<=smax:
        pi.set_servo_pulsewidth(s,int(p))
    elif p>smax:
        p=smax
    elif P<sm:
        p=sm
    return p
    

host = ''
port = args.PUF_port
bufsize = 1024 
addr = (host,port)
udpServer = socket(AF_INET,SOCK_DGRAM) 
udpServer.bind(addr)

while 1:
        data,addr = udpServer.recvfrom(bufsize) 
        data=data.decode() 
        if data == "out":
            stop()
            udpServer.close() 
            print("FPS Out")
            break
        elif data == "mid":
            mid()
        else:
            try:
                data=data.split(";")
                data_1=data[0]
                data_2=data[1]
                ps_1=ps_1-int(data_1)*res_X
                ps_2=ps_2+int(data_2)*res_Y
                ps_1=set_p(s1,ps_1,s1_min,s1_max)
                ps_2=set_p(s2,ps_2,s2_min,s1_max)
            except:
                pass
exit(0)
