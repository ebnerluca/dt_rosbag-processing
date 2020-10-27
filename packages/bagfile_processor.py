import rosbag
import os
import cv2
from cv_bridge import CvBridge

bag_file_name = os.environ['BAG_FILE_NAME']
robot_name = os.environ['ROBOT_NAME']
topic_name = "/" + robot_name + "/camera_node/image/compressed"
dir_name = os.path.dirname(__file__)
bag_file_dir = os.path.join(dir_name, 'bagfiles/')

#bagfiles
bag = rosbag.Bag(bag_file_dir + bag_file_name)
#processed_bag = rosbag.Bag(bag_file_dir + 'processed_bag.bag', 'w')

print("Processing image message from topic " + topic_name + " ...")

with rosbag.Bag(bag_file_dir + 'processed_bag.bag', 'w') as processed_bag:
	for topic, msg, t in bag.read_messages(topics=[topic_name]):
	
		# Extract the timestamp from the message
		timestamp = t
		# Extract the image data from the message
		cv_bridge = CvBridge()
		cv_image = cv_bridge.compressed_imgmsg_to_cv2(msg)

		# Draw the timestamp on top of the image
		font = cv2.FONT_HERSHEY_SIMPLEX
		org = (5, cv_image.shape[0]-5)
		fontScale = 1
		color = (255, 0, 0)#blue
		thickness = 2
		processed_image = cv2.putText(cv_image, str(timestamp), org, font, fontScale, color, thickness)

		# Write the new image to the new bag file, with the same topic name, same timestamp, and the same message type as the original message
		msg_processed = cv_bridge.cv2_to_compressed_imgmsg(processed_image)
		processed_bag.write(topic, msg_processed, timestamp)

bag.close()
processed_bag.close()

print("Processing done! Output file processed_bag.bag can be found in the mounted volume.")