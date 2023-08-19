#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError
import cv2
import os
import csv


class ImageConvertor:
    
    def __init__(self,save_folder,output_file,i):
        self.i=i
        self.bridge=CvBridge()
        self.sub=rospy.Subscriber("/camera/color/image_raw",Image,self.callback)
        rate = rospy.Rate(30)
        self.output_file = output_file
        self.csv_file = open(self.output_file, 'w')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Sequence','Timestamp'])

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
    def callback(self,msg):
        try:
            sequence=msg.header.seq
            timestamp=msg.header.stamp.to_sec()
            self.csv_writer.writerow([sequence,timestamp])


            cv_image=self.bridge.imgmsg_to_cv2(msg,'bgr8')

            image_filename = os.path.join(save_folder, f'image_{sequence-self.i}.jpg')
            cv2.imwrite(image_filename, cv_image)
            rospy.loginfo(f"Saved image: {image_filename}")
        except CvBridgeError as e:
            rospy.logerr(e)



if __name__=="__main__":
    i=0
    rospy.init_node("Image_msg_to_images_node")
    save_folder = os.path.expanduser('~/saved_images')  # Change this to your desired folder path
    t1=rospy.Time.now()
    output_file = os.path.expanduser('~/image_data.csv') 
    image_converter = ImageConvertor(save_folder,output_file,i)
    try:
        i+=1
        rospy.spin()
    except KeyboardInterrupt:
        t2=rospy.Time.now()
        print("Shutting down... %f",t2-t1)