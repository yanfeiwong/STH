import smbus
import math
import time
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
def read_byte(adr):
        return bus.read_byte_data(address, adr)
def read_word(adr):
        high = bus.read_byte_data(address, adr)
        low = bus.read_byte_data(address, adr+1)
        val = (high << 8) + low
        return val
def read_word_2c(adr):
        val = read_word(adr)
        if (val >= 0x8000):
                return -((65535 - val) + 1)
        else:
                return val
def dist(a,b):
        return math.sqrt((a*a)+(b*b))
def get_y_rotation(x,y,z):
        radians = math.atan2(x, dist(y,z))
        return -math.degrees(radians)
def get_x_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)
bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68             # This is the address value read via the i2cdetect command
# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)
tst=0
gxoff=gyoff=gzoff=0

 
t=time.time()
i=0
flag=0
dx0=dy0=dz0=0
'''

while 1:
 i=i+1
 gyro_xout = read_word_2c(0x43)
 gyro_yout = read_word_2c(0x45)
 gyro_zout = read_word_2c(0x47)

 gxoff=0.5*(gxoff+gyro_xout)
 gyoff=0.5*(gyoff+gyro_yout)
 gzoff=0.5*(gzoff+gyro_zout)


 if i==5000:
         break
'''
gxoff=-18.8993978
gyoff=-42.5170139
gzoff=86.0028605
t=time.time()
i=0
while 1:
 i=i+1
 gyro_xout = read_word_2c(0x43)
 gyro_yout = read_word_2c(0x45)
 gyro_zout = read_word_2c(0x47)


 accel_xout = read_word_2c(0x3b)
 accel_yout = read_word_2c(0x3d)
 accel_zout = read_word_2c(0x3f)
 accel_xout_scaled = accel_xout / 16384.0
 accel_yout_scaled = accel_yout / 16384.0
 accel_zout_scaled = accel_zout / 16384.0

 
 t1=time.time()
 dx=dx0+(gyro_xout/131.0-gxoff/131.0)*(t1-t)
 #print(dx-dx0)
 dy=dy0+(gyro_yout/131.0-gyoff/131.0)*(t1-t)
 dz=dz0+(gyro_zout/131.0-gzoff/131.0)*(t1-t)


 if dx>180:
         dx=-360+dx
 elif dx<-180:
         dx=360+dx
 if dy>180:
         dy=dy-360
 elif dy<-180:
         dy=dy+360
 if dz>180:
         dz=dz-360
 elif dz<-180:
         dz=dz+360
 dx0=dx
 dy0=dy
 dz0=dz
 print(int(dx),int(dy),int(dz) )
 #print(dx,dy,dz)
 #print(read_word_2c(0x41))
 t=time.time()
 
 
