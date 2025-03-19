#!/usr/bin/env python2
import serial
import time
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2 
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import os
import binascii
import sys
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

sava_data = int(sys.argv[1])
# Setup paths
base_path = str(Path().absolute()) + "/Data_Robot/{}".format(sava_data)
if not os.path.exists(base_path):
    os.makedirs(base_path)

# Global variables
TouchArray = []
bridge = CvBridge()
save_images = False
start_time = None
frame_count = 0  # Keep track of frame indices
sensorList = []  # Define sensorList globally

# Initialize sensorList
filenameList = [filename for filename in os.listdir('/dev') if filename.startswith('ttyUSB')]
filenameList.sort()
print("USB PORTS:\n", filenameList)

for i, filename in enumerate(filenameList):
    ser = serial.Serial("/dev/{}".format(filename), 115200, timeout=0)
    sensorList.append(ser)

def touch():
    """Collects touch data and ensures alignment with frames."""
    global TouchArray
    dataArray = []
    
    for ser in sensorList:
        ser.write(serial.to_bytes([0x01, 0x00, 0x01]))
        raw_data = ser.read(100)
        data = binascii.hexlify(raw_data)
        
        splittedData = [data[i:i+2] for i in range(0, len(data), 2)]
        if len(splittedData) >= 11:
            touch_values = [int(j, 16) for j in splittedData[2:-1]]
            dataArray.append(touch_values)
    
    if dataArray:
        j = 0
        for i in dataArray[1]:
            if i > 180:
                sense = 2
                j = 1
            elif i > 5 and i<=180 and j==0: # i > 5 because of noise
                sense = 1
                j = 1
            elif i < 5 and j == 0:
                sense = 0
        flattened_data = ' '.join(map(str, dataArray[1]))  # Convert list to space-separated string
        TouchArray.append("{} {}".format(flattened_data, sense))  # Store with frame index

def callback(msg):
    """Handles incoming frames and synchronizes touch data."""
    global save_images, start_time, frame_count
    
    try:
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
    except Exception as e:
        rospy.logerr("Could not convert image: %s", str(e))
        return

    cv2.imshow("Color Image", cv_image)
    cv2.waitKey(1)
    
    if save_images:
        elapsed_time = time.time() - start_time
        if elapsed_time <= 10:
            filename = os.path.join(base_path, "frame_{}.png".format(frame_count))
            cv2.imwrite(filename, cv_image)
            rospy.loginfo("Saved: {}".format(filename))
            
            touch()  # Ensure each frame has a corresponding touch sample
            frame_count += 1  # Increment frame index
        else:
            rospy.loginfo("Finished saving frames.")
            with open(base_path + "/touch_data.txt", "w") as f:
                for data in TouchArray:
                    f.write("{}\n".format(data))
            save_images = False

def main():
    global save_images, start_time, frame_count
    
    rospy.init_node("image_listener", anonymous=True)
    rospy.Subscriber("/torobo/head/camera/color/image_raw", Image, callback)
    
    rospy.sleep(3)
    save_images = True
    start_time = time.time()
    rospy.loginfo("Started saving frames for 10 seconds.")
    
    rospy.spin()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
