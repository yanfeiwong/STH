import rospy,os
from std_msgs.msg import String
from socket import *


host = ''
port = 9921 
bufsize = 1024 
addr = (host,port)
udpServer = socket(AF_INET,SOCK_DGRAM) 
udpServer.bind(addr)


def talker():
    pub = rospy.Publisher('Bot_CC',String, queue_size=10)
    rospy.init_node('Bot',anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        data,addr = udpServer.recvfrom(bufsize) 
        data=data.decode()
        para_str = "para %s" % rospy.get_time()
        rospy.loginfo(para_str)
        pub.publish(para_str)
        rate.sleep()
try:
    
    talker()
    #os.system('roscore')
except rospy.ROSInterruptException:
    pass

