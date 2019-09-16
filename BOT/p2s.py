import math,time,sys
from time import sleep
from picamera import PiCamera
from socket import *
from io import BytesIO

C_RES_X=640
C_RES_Y=480
C_ISO=1200
C_FRR=40
C_hflip=True
C_vflip=True
host  = '192.168.3.17'
port = 9922
bufsize = 1024.0
addr = (host,port)
udpClient = socket(AF_INET,SOCK_DGRAM)




with PiCamera() as camera:
    camera.resolution=(C_RES_X,C_RES_Y)
    camera.framerate=C_FRR
    camera.iso=C_ISO
    camera.hflip=C_hflip
    camera.vflip=C_vflip
    stream=BytesIO()
    for foo in camera.capture_continuous(stream,"jpeg",quality=20,use_video_port=True):#resize=(1080,360),
        size=sys.getsizeof(stream)
        stream.seek(0)
        udpClient.sendto(("sta").encode(),addr)
        cut=int(math.ceil(size)/(bufsize))
        strr="size;"+str(cut)
        udpClient.sendto(strr.encode(),addr)
        for i in range(cut):
            d=stream.read(int(bufsize))
            udpClient.sendto(d,addr)
        udpClient.sendto(("end").encode(),addr)
        stream.seek(0)
        stream.truncate()

