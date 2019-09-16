import Bot_GPIO
from socket import *
Max_P=300.0
Power=0.0
Speed_D=0
res=0.5
host = ''
port = 124 
bufsize = 1024 
addr = (host,port)
udpServer = socket(AF_INET,SOCK_DGRAM) 
udpServer.bind(addr)
Bot_GPIO.stop()
while 1: 
    data,addr = udpServer.recvfrom(bufsize) 
    data=data.decode() 
    if data == "out": 
        udpServer.close() 
	print("Power Out")
        exit(0) 
    else:
        try:
            data=data.split(";")
            data_1=int(data[0])
            data_2=int(data[1])
            Power=int((data_1**2+data_2**2)**0.5/Max_P*100)
            if Power>Max_P:
                Power=Max_P
            if data_2>=0:
                Power=-Power
            left=int((Max_P-data_1*res)*(Power/Max_P))
            right=int((Max_P+data_1*res)*(Power/Max_P))
            if left>100:
                left=100
            if right>100:
                right=100
            Bot_GPIO.setMotor(left, right)
        except:
            pass

