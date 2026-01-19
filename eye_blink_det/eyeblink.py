# Importing the necessary libraries
import cv2
import dlib
import time
from scipy.spatial import distance as dist
import imutils
from imutils import face_utils
from playsound import playsound
import pycurl
from urllib.parse import urlencode
#import pywhatkit
import pyttsx3
from utils import eye_aspect_ratio

def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    # engine.setProperty('rate', 150)  # Speed of speech (words per minute)
    # engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    # Convert text to speech
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()

"""
# Defining a function to compute the eye aspect ratio
def eye_aspect_ratio(eye):
    # Computing the euclidean distances between the two sets of vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Computing the euclidean distance between the horizontal eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # Computing the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # Returning the eye aspect ratio
    return ear"""
	
def send_mail(mail,msg):

	crl = pycurl.Curl()
	crl.setopt(crl.URL, 'https://alc-training.in/gateway.php')
	data = {'email': mail,'msg':msg}
	pf = urlencode(data)

	# Sets request method to POST,
	# Content-Type header to application/x-www-form-urlencoded
	# and data to send in request body.
	crl.setopt(crl.POSTFIELDS, pf)
	crl.perform()
	crl.close()



#def send_mail(mail,msg):
 #   pywhatkit.sendwhatmsg_instantly('+918289879309', msg, 15)




def start(email_id):
    # Initializing the dlib face detector and the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("eye_blink_det/shape_predictor_68_face_landmarks.dat")

    # Grabbing the indexes of the facial landmarks for the left and right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # Starting the video stream
    cap = cv2.VideoCapture(0)

    # Initializing a variable to store the start time of the eye closure
    start_time = None
    open_start_time = None

    # Initializing a variable to store the blink status
    blink = 0

    sys_status=0

    blink_cnt=0

    select_option=0

    duration=0
    dur=0

    ui_path="eye_blink_det/UI/main_menu/1.png"

    # Looping over the frames from the video stream
    while True:
        # Grabbing the frame from the threaded video file stream, resizing it, and converting it to grayscale
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        # Detecting faces in the grayscale frame
        rects = detector(gray, 0)

        # Looping over the face detections
        for rect in rects:
            # Determining the facial landmarks for the face region, then converting the facial landmark (x, y)-coordinates to a NumPy array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # Extracting the left and right eye coordinates, then using the coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # Averaging the eye aspect ratio together for both eyes
            time.sleep(0.25)
            ear = (leftEAR + rightEAR) / 2.0
            #print(ear)

            # Computing the convex hull for the left and right eye, then visualizing each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            

            # Checking if the eye aspect ratio is below a threshold
            
            print("details:","\nsys_status:",sys_status,"select_option:",select_option,"blink_cnt:",blink_cnt,"duration:",duration)
            if ear < 0.25:
                open_start_time = None
                # If the start time is None, initialize it
                if start_time is None:
                    start_time = time.time()
                # Otherwise, check if the eye is closed for 4 seconds
                elif sys_status==0:
                    duration = time.time() - start_time
                    dur = time.time() - start_time
                    if duration >= 4:
                        # Set the blink status to 1
                        blink = 1
                        # Break out of the loop
                        #print("1.Entertainment\n2.Prebuilt messages\n3.food menu\n4.Washroom Option:\n")
                        ui_path="eye_blink_det/UI/main_menu/1.png"

                        
                        #time.sleep(10) # Wait for 10 seconds before exiting the blink check and initiating the menu function
                        sys_status=1
                        start_time = time.time()
                        #exit(0) # Add menu function instead of exit
                        #break
                        #break
                elif sys_status==1: 
                    print("flg1")
                    duration = time.time() - start_time
                    dur = time.time() - start_time
                    if duration >= 4:
                        blink_cnt+=1
                        #if select_option==3:
                        #    select_option=0
                         #   blink_cnt=0
                        #print("blink cnt:",blink_cnt)
                        start_time = time.time()
                        #print("flg2")
                        if select_option==0:
                            if blink_cnt==4:
                                blink_cnt = 0
                                #print("flg3")
                        if select_option==1:
                            if blink_cnt==5:
                                blink_cnt = 0
                                #print("flg9")
                        if select_option==2:
                            if blink_cnt==17:
                                blink_cnt = 0
                                #print("flg9")
                        if select_option==3:
                            if blink_cnt==8:
                                blink_cnt = 0
                                #print("flg9")

                    
                    #if dur>20:
                    #    exit()
                
                    

                    """if duration >= 10:
                        if blink_cnt==1:
                            print("play music")
                        elif blink_cnt==2:
                            print("prebuilt messages")
                        elif blink_cnt==3:
                            print("option 3")
                        elif blink_cnt==4:
                            print("option 4")"""
                        



                    """
                        
                        print("playing music")
                        playsound('test.wav')
                        start_time = time.time()
                    if duration >= 4:
                        sys_status=0"""
                        
                
            # Otherwise, reset the start time and blink status
            else:
                if open_start_time is None:
                    open_start_time = time.time()
                    print("flg4")
                start_time = None
                blink = 0
                dur=0
                print("flg5")

                if sys_status==1:
                    open_duration = time.time() - open_start_time
                    print("flg6")
                    if open_duration>=4:
                        print("flg7")
                        if select_option==0:
                            if blink_cnt==1:
                                select_option=1
                                print("Emergency")
                                blink_cnt=0

                            elif blink_cnt==2:
                                select_option=2
                                print("prebuilt Messages")
                                blink_cnt=0
                                #ui_path="UI/main_menu/3.jpg"
                                #exit()

                            elif blink_cnt==3:
                                select_option=3
                                print("Food menu")
                                blink_cnt=0
                                #ui_path="UI/main_menu/4.jpg"
                                #exit()
                                   
                            #elif blink_cnt==4:
                                #select_option=4
                                #print("play music")
                                #playsound('test.wav')
                                #blink_cnt=0
                                #ui_path="UI/main_menu/2.jpg"    
                                #exit()
                                #ui_path="UI/main_menu/5.jpg"
                                #exit()

                        if select_option==1:
                            if blink_cnt==1:
                                msg="send message: Medical Assistance"
                                print(msg)
                                send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==2:
                                msg="send message: Emergency Help"
                                print(msg)
                                send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==3:
                                msg="send message: Fire Emergency"
                                print(msg)
                                send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==4:
                                msg="send message:Intruder/Suspect"
                                print(msg)
                                send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0

                        if select_option==2:
                            if blink_cnt==1:
                                msg="send message:YES"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==2:
                                msg="send message:NO"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==3:
                                msg="send message:Good Morning"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==4:
                                msg="send message:Good Night"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==5:
                                msg="send message:How are you?"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==6:
                                msg="send message: How is your Family?"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==7:
                                msg="send message: I am Good."
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==8:
                                msg="send message: I am not Well."
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==9:
                                msg="send message: I feel Sad"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==10:
                                msg="send message: I don't want to see you."
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==11:
                                msg="send message: Bye!"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==12:
                                msg="send message: I don't want anything to eat."
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==13:
                                msg="send message: What?"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==14:
                                msg="send message: Where?"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==15:
                                msg="send message: Whom?"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==16:
                                msg="send message: Why?"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0

                        if select_option==3:
                            if blink_cnt==1:
                                msg="send message: Porridge"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==2:
                                msg="send message: Hot Water"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==3:
                                msg="send message: Cold Water"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==4:
                                msg="send message: Milk"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==5:
                                msg="send message: Tea"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==6:
                                msg="send message: Coffee"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0
                            elif blink_cnt==7:
                                msg="send message: Juice"
                                print(msg)
                                #send_mail(email_id,msg)
                                text_to_speech(msg)
                                sys_status=0
                                select_option=0
                                blink_cnt=0

                        if select_option==4:
                            playsound('test.wav')
                            sys_status=0
                            select_option=0
                            blink_cnt=0
                #if blink_cnt>5:
                #    print("flg8")
                #    blink_cnt=0
                        
                            #print("prebuilt messages:\n1. i am ok\n2. i want to eat\n3.i am feeling bad\n4.i want water\n5. i want to see my daughter")
                            
                            #exit()
                        
            
                #playsound('test.wav')
                # Set the blink status to 1
                # blink = 1
                # Break out of the loop
                #print("1.Entertainment\n2.Prebuilt messages\n3.Washroom Option\n4.Water\\foodoption:\n")
            #print(blink)

            # Displaying the blink status on the frame
        if select_option==0:
            if blink_cnt==0:
                ui_path="eye_blink_det/UI/main_menu/1.png"
            elif blink_cnt==1:
                ui_path="eye_blink_det/UI/main_menu/2.png"
            elif blink_cnt==2:
                ui_path="eye_blink_det/UI/main_menu/3.png"
            elif blink_cnt==3:
                ui_path="eye_blink_det/UI/main_menu/4.png"
            elif blink_cnt==4:
                ui_path="eye_blink_det/UI/main_menu/5.png"
                blink_cnt=1

        if select_option==1:
            if blink_cnt==0:
                ui_path="eye_blink_det/UI/emergency_menu/1.png"
            elif blink_cnt==1:
                ui_path="eye_blink_det/UI/emergency_menu/2.png"
            elif blink_cnt==2:
                ui_path="eye_blink_det/UI/emergency_menu/3.png"
            elif blink_cnt==3:
                ui_path="eye_blink_det/UI/emergency_menu/4.png"
            elif blink_cnt==4:
                ui_path="eye_blink_det/UI/emergency_menu/5.png"
            #elif blink_cnt==4:
                #ui_path="UI/main_menu/5.png"
        if select_option==2:
            if blink_cnt==0:
                ui_path="eye_blink_det/UI/message_menu/1.png"
            elif blink_cnt==1:
                ui_path="eye_blink_det/UI/message_menu/2.png"
            elif blink_cnt==2:
                ui_path="eye_blink_det/UI/message_menu/3.png"
            elif blink_cnt==3:
                ui_path="eye_blink_det/UI/message_menu/4.png"
            elif blink_cnt==4:
                ui_path="eye_blink_det/UI/message_menu/5.png"
            elif blink_cnt==5:
                ui_path="eye_blink_det/UI/message_menu/6.png"
            elif blink_cnt==6:
                ui_path="eye_blink_det/UI/message_menu/7.png"
            elif blink_cnt==7:
                ui_path="eye_blink_det/UI/message_menu/8.png"
            elif blink_cnt==8:
                ui_path="eye_blink_det/UI/message_menu/9.png"
            elif blink_cnt==9:
                ui_path="eye_blink_det/UI/message_menu/10.png"
            elif blink_cnt==10:
                ui_path="eye_blink_det/UI/message_menu/11.png"
            elif blink_cnt==11:
                ui_path="eye_blink_det/UI/message_menu/12.png"
            elif blink_cnt==12:
                ui_path="eye_blink_det/UI/message_menu/13.png"
            elif blink_cnt==13:
                ui_path="eye_blink_det/UI/message_menu/14.png"
            elif blink_cnt==14:
                ui_path="eye_blink_det/UI/message_menu/15.png"
            elif blink_cnt==15:
                ui_path="eye_blink_det/UI/message_menu/16.png"
            elif blink_cnt==16:
                ui_path="eye_blink_det/UI/message_menu/17.png"
        if select_option==3:
            if blink_cnt==0:
                ui_path="eye_blink_det/UI/food_menu/1.png"
            elif blink_cnt==1:
                ui_path="eye_blink_det/UI/food_menu/2.png"
            elif blink_cnt==2:
                ui_path="eye_blink_det/UI/food_menu/3.png"
            elif blink_cnt==3:
                ui_path="eye_blink_det/UI/food_menu/4.png"
            elif blink_cnt==4:
                ui_path="eye_blink_det/UI/food_menu/5.png"
            elif blink_cnt==5:
                ui_path="eye_blink_det/UI/food_menu/6.png"
            elif blink_cnt==6:
                ui_path="eye_blink_det/UI/food_menu/7.png"
            elif blink_cnt==7:
                ui_path="eye_blink_det/UI/food_menu/8.png"

        #print("UI PATH",ui_path)
        
        img = cv2.imread(ui_path, cv2.IMREAD_COLOR)
        resized_image = cv2.resize(img, (1080, 720))
        #print("duration:",duration)
        cv2.putText(resized_image,"sys_status:{},option: {},duration: {}".format(sys_status,blink_cnt,duration), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Showing the frame
        cv2.imshow("Frame", resized_image)
        key = cv2.waitKey(1) & 0xFF

        # If the `q` key was pressed, break from the loop
        if key == ord('q'):
            break

    # Do a bit of cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start("joelvarghese656@gmail.com")