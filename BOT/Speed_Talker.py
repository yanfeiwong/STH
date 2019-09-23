####Optocoupler speed measurement####
import RPi.GPIO as GPIO
import time,rospy
from std_msgs.msg import String

Rate=60

L_P=23
R_p=26
L_Stat=0
R_Stat=0
L_Count=0
R_Count=0
L_T0=0
L_T2=0
R_T0=0
R_T2=0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(L_P, GPIO.IN)
GPIO.setup(R_P, GPIO.IN)

pub = rospy.Publisher('Speed',String, queue_size=10)
rospy.init_node('talker',anonymous=True)
rate = rospy.Rate(Rate)

def if_diff(pin):
    global L_Stat,R_Stat
    if pin == L_P:
        L = GPIO.input(L_P)
        if L == L_Stat:
            return 0
        else:
            L_Stat= L
            return 1
    elif pin == R_P:
        R = GPIO.input(R_P)
        if R == R_Stat:
            return 0
        else:
            R_Stat= R
            return 1
        
def print_speed(L_R,T0,T2):
    speed_str=L_R+";"+str(1.0/20/(T2-T1))
    rospy.loginfo(speed_str)#
    pub.publish(speed_str)
    
while 1:
    if L_Count == 0:
        L_T0 = time.time()
    if R_Count == 0:
        R_T0 = time.time()
    if if_diff(L_P):
        L_Count = L_Count+1
    if if_diff(R_P):
        R_Count = R_Count+1
    if L_Count == 2:
        L_Count = 0
        L_T2 = time.time()
        print_speed("l",L_T0,L_T2)
        L_T0 = L_T2
    if R_Count == 2:
        R_Count = 0
        R_T2 = time.time()
        print_speed("l",R_T0,R_T2)
        R_T0 = R_T2
    rate.sleep()#
        
