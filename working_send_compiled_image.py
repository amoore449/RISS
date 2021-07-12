import sys
import cv2
import os.path
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def image_check():
    #test that enough images are provided for the
    if (len(sys.argv) < 3):
        print("Usage: testvideo <rate in Hz> <list of images>")
        return 0

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
    image_terms = ["background"]
    #Format size of width and height
    width = 400
    height = 300

    new_path = os.path.join(script_dir, background)
    new_path = PILimage.open(new_path)
    new_path = new_path.convert("RGB")
    image_names.append(new_path)

    #Create ros images for the file system
    ros_images  = []
    rospack = rospkg.RosPack()
    image_path = rospack.get_path('quori_gazebo') + '/images/'

    #cycle through images and convert to ROS msg (These might need to be fixed)
    for i, arg in enumerate(image_names):
        print("Converting " + image_terms[i] + " to ROS msg")
        pil_image = image_names[i]

        #Convert to Color format appropriate for cv2
    	opencvImage = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
        bridge = CvBridge()
        cv_img = numpy.array(pil_image)

        #Convert image cv2 image to image message for ROS
        image_message = bridge.cv2_to_imgmsg(cv_img, "bgr8") #if this doesn't work try bgra8
        ros_images.append(image_message)
        period = float(rate)

    nimage = 0
    num_images = 1
    
    # While not shutdown ROS will run ros_images and image_terms loop
    while not rospy.is_shutdown():
        #signal which image is being sent to ROS
        print("Sending Image " + image_terms[i] + " to ROS msg")
        #publish image to ROS and then wait
        pub.publish(ros_images[nimage])
        time.sleep(period)
        #Establish term for nimage
      	nimage = (nimage+1)%num_images

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


    script_dir = os.path.dirname(os.path.abspath(__file__))
    background = PILimage.open(os.path.join(script_dir, 'background.jpg'))
    background = background.convert("RGBA")

    eye_motions = [l_1,l_2, l_3, l_4, l_5, l_6, r_1, r_2, r_3, r_4, r_5,r_6]
    lid_array = [left_pupil, l_6, left_spot, right_pupil, r_6, right_spot]
    x_multiplier = [.7, .5, .8,  .2, .05, .3]
    y_multiplier = [.3, .25, .4, .3, .25, .4]


    i = 0
    for x in lid_array:
        my_image = PILimage.open(os.path.join(script_dir, x))
        my_image = my_image.resize((int(my_image.size[0]*0.4), int(my_image.size[1]*0.4)))
        if i ==2 or i == 5:
            my_image = my_image.resize((int(my_image.size[0]*0.1), int(my_image.size[1]*0.1)))
        my_image = my_image.convert("RGBA")
        width = background.width
        height = background.height
        width = int(width*x_multiplier[i])
        height = int(height*y_multiplier[i])
        this_background = background.paste(my_image, (width, height), my_image)

        background.save(os.path.join(script_dir, "pnew.png"), format="png")
        i = i +1

if __name__ == '__main__':
    image_process()
    picture_send("pnew.png")
    #main()
