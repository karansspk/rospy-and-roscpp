#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
import csv
import os 

class IMUDataExtractor:
    def __init__(self, output_file):
        self.imu_sub = rospy.Subscriber('/camera/imu', Imu, self.imu_callback)
        self.output_file = output_file
        self.csv_file = open(self.output_file, 'w')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'Velocity_x', 'Velocity_y', 'Velocity_z', 'Acceleration_x', 'Acceleration_y', 'Acceleration_z'])
    
    def imu_callback(self, imu_msg):
        timestamp = imu_msg.header.stamp.to_sec()
        velocity = imu_msg.angular_velocity
        acceleration = imu_msg.linear_acceleration

        self.csv_writer.writerow([timestamp, velocity.x, velocity.y, velocity.z, acceleration.x, acceleration.y, acceleration.z])
    
    def shutdown(self):
        self.csv_file.close()

def main():
    rospy.init_node('Imu_msg_to_csv_node', anonymous=True)
    # output_file = '~/imu_data.csv'  # Change this to your desired CSV file path
    output_file = os.path.expanduser('~/imu_data.csv') 
    imu_extractor = IMUDataExtractor(output_file)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down...")
    
    imu_extractor.shutdown()

if __name__ == '__main__':
    main()
