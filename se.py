import Adafruit_PCA9685,time,os
from socket import *

host = ''
port=9921
bufsize=1024
addr=(host,port)
us=socket(AF_INET,SOCK_DGRAM)
us.bind(addr)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
py_max=545
px_max=700
py_min=145
px_min=145
py_def=py=240
px_def=px=400
pwm.set_pwm(1, 0, int(py_def))
pwm.set_pwm(0, 0, int(px_def))


def p_exit():
    pwm.set_pwm(0, 0, 0)
    pwm.set_pwm(1, 0, 0)
    pwm.set_pwm(2, 0, 0)
    os._exit(0)
def reset():
    global px,py
    px=px_def
    py=py_def
    pwm.set_pwm(1, 0, int(py_def))
    pwm.set_pwm(0, 0, int(px_def))
    
    
while 1:
    try:
        data,addr=us.recvfrom(bufsize)
        data=data.decode()
        if data=="out":
            p_exit()
        if data=="reset":
            reset()
        data=data.split(";")
        ax=int(data[0])
        ay=int(data[1])
        px=px+ax*0.2
        py=py+ay*0.2
        if px>px_max :
            px=px_max
        elif px<px_min:
            px=px_min
        if py>py_max :
            py=py_max
        elif py<py_min:
            py=py_min
        
        pwm.set_pwm(0, 0, int(px))
        pwm.set_pwm(1, 0, int(py))
        #print(py)
    except:
        pass
'''
pwm.set_pwm_freq(60)
pwm.set_pwm(0, 0, 200)
time.sleep(0.5)
pwm.set_pwm(0, 0, 600)
time.sleep(0.5)
pwm.set_pwm(0, 0, 0)
'''
