import pigpio,time,smbus
pi = pigpio.pi()
ma0=14
ma1=15
t=0.005


bus = smbus.SMBus(1)
address = 0x68
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
bus.write_byte_data(address, power_mgmt_1, 0)
#bus.write_byte_data(address, 0x1b, 0x18)
gxoff=gyoff=gzoff=0
dx0=dy0=dz0=dxx0=dzz0=dyy0=0
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

def nsz(s):
    if s<-255:
        s=255
    pi.set_PWM_dutycycle(ma1,255)
    pi.set_PWM_dutycycle(ma0,255-abs(s))
def ssz(s):
    if s>255:
        s=255
    pi.set_PWM_dutycycle(ma0,255)
    pi.set_PWM_dutycycle(ma1,255-s)
def ma(s):
    if s>=0 and s<=255:
        ssz(s)
    elif s<=0 and s>=-255:
        nsz(s)

t=time.time()
while 1:
 gyro_xout = read_word_2c(0x43)
 gyro_yout = read_word_2c(0x45)
 gyro_zout = read_word_2c(0x47)
 t1=time.time()
 dx=dx0+(gyro_xout/131.0-gxoff/131.0)*(t1-t)
 dy=dy0+(gyro_yout/131.0-gyoff/131.0)*(t1-t)
 dz=dz0+(gyro_zout/131.0-gzoff/131.0)*(t1-t)
 if dy>=10:
     ma(0)
 if dy<=10:
     ma(0)
'''
while 1:
    time.sleep(t)
    ma(255)
    time.sleep(t)
    ma(-255)
'''   
