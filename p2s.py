import math,time,sys
from time import sleep
from picamera import PiCamera
from socket import *
from io import BytesIO



host  = '192.168.1.12'
port = 9921
bufsize = 1024.0
addr = (host,port)
udpClient = socket(AF_INET,SOCK_DGRAM)




with PiCamera() as camera:
    camera.resolution=(640,480)
    camera.framerate=40
    camera.iso=400

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

