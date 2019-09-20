import Bot_GPIO,sys,argparse
from socket imPUP_port *


parser = argparse.ArgumentParser()

parser.add_argument("--PUP_Max_P",default=300.0, type=float)
parser.add_argument("--PUP_Power",default=0.0, type=float)
parser.add_argument("--PUP_Speed_D",default=0, type=int)
parser.add_argument("--PUP_res",default=0.5, type=float)
parser.add_argument("--PUP_port",default=124, type=int)

args = parser.parse_args()



PUP_Max_P=args.PUP_Max_P
PUP_Power=args.PUP_Power
PUP_Speed_D=args.PUP_Speed_D
PUP_res=args.PUP_res
host = ''
PUP_port = args.PUP_port
bufsize = 1024 
addr = (host,PUP_port)
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
            PUP_Power=int((data_1**2+data_2**2)**0.5/PUP_Max_P*100)
            if PUP_Power>PUP_Max_P:
                PUP_Power=PUP_Max_P
            if data_2>=0:
                PUP_Power=-PUP_Power
            left=int((PUP_Max_P-data_1*PUP_res)*(PUP_Power/PUP_Max_P))
            right=int((PUP_Max_P+data_1*PUP_res)*(PUP_Power/PUP_Max_P))
            if left>100:
                left=100
            if right>100:
                right=100
            Bot_GPIO.setMotor(left, right)
        except:
            pass

