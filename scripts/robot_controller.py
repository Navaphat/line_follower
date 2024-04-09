#! /usr/bin/env python3
import rospy
from geometry_msgs.msg import Point, Twist
import numpy as np
from sensor_msgs.msg import Image
import math
from gazebo_msgs.msg import ModelStates

class bot_control:
    def __init__(self) :
        self.velocity_msg = Twist()
        self.velocity_msg.linear.y = 0
        self.velocity_msg.linear.z = 0
        self.velocity_msg.angular.x = 0
        self.velocity_msg.angular.y = 0
        self.pub = rospy.Publisher('/spot/cmd_vel' , Twist , queue_size = 10)
        self.state = rospy.Subscriber('/gazebo/model_states', ModelStates, self.callback)
        self.P = 0.004 #rospy.get_param("line_follower_controller/pid/p")
        self._stop = False

    
      #self.image_sub = Line_Follower()

    def callback(self, msg):
        index = msg.name.index("spot")
        x = msg.pose[index].position.x
        y = msg.pose[index].position.y
        z = msg.pose[index].position.z
        if (x >= 1.965639 and x <= 1.972989 and y <= 1.972989 and y >= -3.229230):
            self.stop()

    #move function to move robot
    def move(self,linear,angular):
        self.velocity_msg.linear.x = linear + 0.2
        self.velocity_msg.angular.z = angular
        self.pub.publish(self.velocity_msg)
        
    #fix error & bot position correction
    def fix_error(self, linear_error, orien_error, line_detected):

        if not line_detected:
            self.turn_right()
        else:
            if orien_error < 0:           

                # fixing the yaw     
                self.move(0.5,self.P*orien_error)
                #print("fixing yaw by turning left")

            elif orien_error > 0:           

                # fixing the yaw     
                self.move(0.5,self.P*orien_error)
                #print("fixing yaw by turning right")
                    
            else:
                
                # moving in straight line
                self.move(0.5, 0)
                #print("moving straight")


    def turn_right(self):
         self.move(0, -0.6)
    
    def stop(self):
         rospy.signal_shutdown('Reach the Goal.')

    def turn_left(self):
        self.move(0, 0.6)


  
if __name__=="__main__":
    robot = bot_control()