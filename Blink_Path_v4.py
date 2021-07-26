#!/usr/bin/env python
# license removed for brevity
import rospy
import rospkg
from PIL import Image as PILimage
import time
import numpy as np
import sys
import cv2
import os.path
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import math
import cv2
def malt_overlay_path(multiplier, x_pos_mult, y_pos_mult, image_1, str_foreground, count):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    foreground = os.path.join(script_dir, str_foreground)
    image_3 = cv2.imread(foreground, cv2.IMREAD_UNCHANGED)
    cv2.imwrite("test.jpg", image_3)

    print("________x_multiplier", x_pos_mult)
    print("_________________y_multiplier", y_pos_mult)

    if count == 1:
        ones = np.ones((image_1.shape[0], image_1.shape[1]))*255
        image_1 = np.dstack([image_1, ones])
    ## Smart resizing function
    h, w, c = image_1.shape
    print('width image_1:  ', w)
    print('height image_1: ', h)
    print('channel image_1:', c)

    start_h = int(math.floor(h*y_pos_mult))
    start_w  = int(math.floor(w*x_pos_mult))
    print('width start_w:  ', start_w)
    print('height start_h: ', start_h)

    print("image str_foreground", str_foreground)
    ## Smart resizing function
    h3, w3, c3 = image_3.shape
    print('width image_3:  ', w3)
    print('height image_3: ', h3)
    print('channel image_3:', c3)

    w4 = int(math.floor(w3*multiplier))
    h4 = int(math.floor(h3*multiplier))

    print('width w4:  ', w4)
    print('height h4: ', h4)

    resized_image_3 = cv2.resize(image_3, dsize=(w4, h4))
    h5, w5, c4 = resized_image_3.shape
    print('width w5:  ', w5)
    print('height h5: ', h5)
    print('channel image_3:', c4)

    #image_1[150:250, 150:250] = resized_image_3
    alpha_image_3 = resized_image_3[:, :, 3] / 255.0
    alpha_image = 1 - alpha_image_3
    for c in range(0, 3):
        image_1[start_h:start_h+h5, start_w:start_w+w5, c] = ((alpha_image*image_1[start_h:start_h+h5, start_w:start_w+w5, c]) + (alpha_image_3*resized_image_3[:, :, c]))
    # Filename
    filename = str(count) + 'savedImage.png'
    ## Calculate space left
    print('Space left in image weight:', w-(start_w+w5) )
    print('Space left in image height:', h-(start_h+h5))

    # Using cv2.imwrite() method
    # Saving the image
    print("checking image_1 shape", image_1.shape)
    return image_1



def picture_send(background):
    #Establish Rospack and image path systems
    rospack = rospkg.RosPack()
    rospack.list()
    image_path = rospack.get_path('quori_gazebo') + '/images/'

    #initialize publisher node
    rospy.init_node('testvideo', anonymous=True)
    pub = rospy.Publisher("quori/face_image", Image, queue_size=10)
    rospy.init_node('testvideo', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    #rate of image progression
    rate = .6
    script_dir = os.path.dirname(os.path.abspath(__file__))
    #number of images provided
    num_images = len(sys.argv)-2
    # array of all possible image names and all possible image terms
    image_names = []
    image_terms = []
    #Format size of width and height
    width = 400
    height = 300

    #new_path = os.path.join(script_dir, background)
    #new_path = PILimage.open(new_path)
    count = 0
    for x in background:
        new_path = x
        image_names.append(new_path)
        count = count + 1
        tester = "tester" + str(count)
        image_terms.append(tester)

    #Create ros images for the file system
    ros_images  = []
    rospack = rospkg.RosPack()
    image_path = rospack.get_path('quori_gazebo') + '/images/'

    #cycle through images and convert to ROS msg (These might need to be fixed)
    for i, arg in enumerate(image_names):
        print("Converting " + image_terms[i] + " to ROS msg")
        pil_image = image_names[i]
        pil_image = np.uint8(pil_image)

        #Convert to Color format appropriate for cv2
        opencvImage = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGBA2BGRA)
        bridge = CvBridge()
        cv_img = np.array(pil_image)

        #Convert image cv2 image to image message for ROS
        image_message = bridge.cv2_to_imgmsg(cv_img, "bgra8") #if this doesn't work try bgra8
        ros_images.append(image_message)
        period = float(rate)
    nimage = 0
    num_images = len(ros_images)

    # While not shutdown ROS will run ros_images and image_terms loop
    user_input = "y"
    num_count = 0
    proend = time.time()
    print("complete load time")
    while user_input != "e":
        nimage = (nimage+1)%num_images
        #signal which image is being sent to ROS
        print("Sending Image " + image_terms[nimage] + " to ROS msg")
        #publish image to ROS and then wait
        print("ros images info")
        print(nimage)
        print(len(ros_images))
        pub.publish(ros_images[nimage])
        time.sleep(period)
        num_count = num_count + 1
        if num_count == num_images:
            num_count = 0
            user_input = raw_input("Press e to exit, any other key to continue: ")
            print(user_input)

def resizer(resize_array, new_size, script_dir):
    new_array = []
    for x in resize_array:
        my_image = cv2.imread(os.path.join(script_dir, x), cv2.IMREAD_UNCHANGED)
        #my_image = PILimage.open(os.path.join(script_dir, x))
        width = int(my_image.shape[1] * new_size)
        height = int(my_image.shape[0] * new_size)
        dim = (width, height)
        # resize image
        resized = cv2.resize(my_image, dim, interpolation = cv2.INTER_AREA)
        #my_image = my_image.resize((int(my_image.size[0]*new_size), int(my_image.size[1]*new_size)))
        new_array.append(resized)
    return new_array

'''
image_process
define all relevant images to import and file paths

'''
def image_process():
    left_pupil = "images/pupil.png"
    left_spot = "images/spot.png"
    right_pupil = "images/pupil.png"
    right_spot = "images/spot.png"
    my_background = "images/background.jpg"

    l_6 = "images/6.png"
    l_5 = "images/5.png"
    l_4 = "images/4.png"
    l_3 = "images/3.png"
    l_2 = "images/2.png"
    l_1 = "images/1.png"

    r_6 = "images/right/6.png"
    r_5 = "images/right/5.png"
    r_4 = "images/right/4.png"
    r_3 = "images/right/3.png"
    r_2 = "images/right/2.png"
    r_1 = "images/right/1.png"

    print("Setting Up Facial Features")
    eye_motions = [l_1,l_2, l_3, l_4, l_5, l_6, r_1, r_2, r_3, r_4, r_5,r_6]
    pupils = [left_pupil, right_pupil]
    spots = [left_spot, right_spot]

    script_dir = os.path.dirname(os.path.abspath(__file__))

    lid_array_6 = [pupils[0], eye_motions[5], spots[0], pupils[1], eye_motions[11], spots[1]]
    lid_array_5 = [pupils[0], eye_motions[4], spots[0], pupils[1], eye_motions[10], spots[1]]
    lid_array_4 = [pupils[0], eye_motions[3], spots[0], pupils[1], eye_motions[9], spots[1]]
    lid_array_3 = [pupils[0], eye_motions[2], spots[0], pupils[1], eye_motions[8], spots[1]]
    lid_array_2 = [pupils[0], eye_motions[1], spots[0], pupils[1], eye_motions[7], spots[1]]
    lid_array_1 = [pupils[0], eye_motions[0], spots[0], pupils[1], eye_motions[6], spots[1]]

    #Compiled image of lid_array
    picture_array = [lid_array_1, lid_array_2, lid_array_3, lid_array_4, lid_array_5, lid_array_6]


    #Shift through iterations
    x_multiplier = [.7, .5, .8,  .2, .05, .3]
    y_multiplier = [.3, .25, .4, .3, .25, .4]

    #create shift amount
    shift_amount = .1
    i = 0
    image_consol = []
    #Find number of iterations
    it_num = shift_amount/.01
    my_counter = 0
    script_dir = os.path.dirname(os.path.abspath(__file__))
    str_background = os.path.join(script_dir, "background1.jpg")
    count = 0
    for y in picture_array:
        background = cv2.imread(str_background)
        background = image_process_value(y, my_counter, x_multiplier, y_multiplier, script_dir, background)
        newer_names = str(my_counter) + "et_new.png"
        image_consol.append(background)
        my_counter = my_counter + 1
    return image_consol

def image_process_value(picture_array, my_counter, x_multiplier, y_multiplier, script_dir, background):
    i = 0
    count = 0
    image_1 = background
    for x in picture_array:
        x_pos_mult  = x_multiplier[count]
        y_pos_mult = y_multiplier[count]
        count = count + 1
        #image_3 = cv2.imread(str(x), cv2.IMREAD_UNCHANGED)
        #alt_overlay_path(multiplier, x_pos_mult, y_pos_mult, image_1, str_foreground, count):
        if (count == 3 or count == 6):
            multiplier = .05
        else:
            multiplier = .4
        image_1 = malt_overlay_path(multiplier, x_pos_mult, y_pos_mult, image_1, str(x), count)
        # Filename
    filename = str(count) + 'savedImage.png'
    return image_1

if __name__ == '__main__':
    background = image_process()
    picture_send(background)
