import rospy,os,smbus,math,time
from std_msgs.msg import String



Rate=30
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
bus = smbus.SMBus(1)
address = 0x68

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

def talker():
    global dx0,dy0,dz0,t
    pub = rospy.Publisher('MPU',String, queue_size=10)
    rospy.init_node('talker',anonymous=True)
    rate = rospy.Rate(Rate)
    while not rospy.is_shutdown():
        gyro_xout = read_word_2c(0x43)
        gyro_yout = read_word_2c(0x45)
        gyro_zout = read_word_2c(0x47)
        t1=time.time()
        dx=dx0+(gyro_xout/131.0-gxoff/131.0)*(t1-t)
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
        mpu_str = str(int(dx))+","+str(int(dy))+","+str(int(dz))
        rospy.loginfo(mpu_str)
        pub.publish(mpu_str)
        t=time.time()
        rate.sleep()
        

bus.write_byte_data(address, power_mgmt_1, 0)
t=time.time()
dx0=dy0=dz0=0
gxoff=-18.8993978
gyoff=-42.5170139
gzoff=86.0028605
t=time.time()

try:
    
    talker()
    #os.system('roscore')
except rospy.ROSInterruptException:
    pass
