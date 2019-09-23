####Cmaera/Image live stream management####
import math,time,sys,argparse
from time import sleep
from picamera import PiCamera
from socket import *
from io import BytesIO

parser = argparse.ArgumentParser()

parser.add_argument("--C_RES_X",default=640, type=int)
parser.add_argument("--C_RES_Y",default=480, type=int)
parser.add_argument("--C_ISO",default=1200, type=int)
parser.add_argument("--C_FRR",default=40, type=int)
parser.add_argument("--C_hflip", type=str2bool, nargs='?',
                        const=True, default=True)
parser.add_argument("--C_vflip", type=str2bool, nargs='?',
                        const=True, default=True)
parser.add_argument("--C_host",default='192.168.3.17')
parser.add_argument("--C_port",default=9922, type=int)

args = parser.parse_args()

C_RES_X = args.C_RES_X
C_RES_Y = args.C_RES_Y
C_ISO = args.C_ISO
C_FRR = args.C_FRR
C_hflip = args.C_hflip
C_vflip = args.C_vflip
host  = args.C_host
port = args.C_port
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

