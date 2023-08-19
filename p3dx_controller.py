import rospy 
from geometry_msgs.msg import Twist
import keyboard
import subprocess
from pynput import keyboard

def on_press(key):
    msg=Twist()
    global k
    if key==keyboard.Key.up:
        rospy.loginfo("Up Arrow pressed. Executing command...")
        msg.linear.x=k
        k=k+0.2
        if(msg.linear.x>0.6):
            k=0
            msg.linear.x=0
            msg.angular.z=0
        pub.publish(msg)

    elif key==keyboard.Key.down:
        rospy.loginfo("Down Arrow pressed. Executing command...")
        msg.linear.x=k
        k=k-0.2
        if(msg.linear.x>0.5):
            k=0
            msg.linear.x=0
            msg.angular.z=0
        pub.publish(msg)

    elif key==keyboard.Key.right:
        rospy.loginfo("Right Arrow pressed. Executing command...")
        msg.angular.z=k
        k=k-0.2
        if(msg.angular.z<-0.8):
            k=0
            msg.linear.x=0
            msg.angular.z=0
        pub.publish(msg)  

    elif key == keyboard.Key.space:
        rospy.loginfo("Spacebar pressed. Executing command...")
        msg.linear.x=0
        msg.angular.z=0
        k=0
        pub.publish(msg)

    elif key == keyboard.Key.left:
        rospy.loginfo("Left Arrow pressed. Executing command...")
        msg.angular.z=k
        k=k+0.2
        if(msg.angular.z>0.8):
            k=0
            msg.linear.x=0 
            msg.angular.z=0
        pub.publish(msg)  


if __name__=='__main__':
    rospy.init_node("p3dx_controller")
    k=0
    pub=rospy.Publisher("/RosAria/cmd_vel",Twist,queue_size=10)
    # subprocess.call(['sudo', 'python', 'p3dx_controller.py'])
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    rospy.spin()
    

