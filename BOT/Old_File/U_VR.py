import pigpio,os,time
from socket import *

try:
    os.system("sudo pigpiod")
    tim.sleep(2)
except:
    pass

res_X=1.0
res_Y=1.2
res_VR=4
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
data_1_old=''
data_2_old=''
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
port = 127
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
            print("VR Out")
            break
        elif data == "mid":
            mid()
        else:
            try:
                data=data.split(";")
                data_1=data[0]
                data_2=data[1]
                if data_1!='':
                    if data_1_old =='':
                        data_1_old=data_1
                    else:
                        pm_2=int(data_1)-int(data_1_old)
                        data_1_old=data_1
                        if int(data_2_old)>180:
                            ps_2=ps_2-pm_2*res_VR
                        else:
                            ps_2=ps_2+pm_2*res_VR
                        ps_2=set_p(s2,ps_2,s2_min,s2_max)
                if data_2!='':
                    if data_2_old =='':
                        data_2_old=data_2
                    else:
                        pm_1=int(data_2)-int(data_2_old)
                        data_2_old=data_2
                        #ps_1=ps_1-pm_1*res_VR
                        #ps_1=set_p(s1,ps_1,s1_min,s1_max)
                #print(data_1)
                #print(data_2)
            except:
                pass
