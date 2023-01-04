import os
import dlib
from PIL import Image
import numpy as np
from skimage import io
import cv2
from datetime import datetime
import pandas as pd 
from sqlalchemy import create_engine
import pymysql
import random
import time
import sqlalchemy
#import RPi.GPIO as GPIO

work_dir = os.getcwd()
data_dir = os.path.expanduser(work_dir)
#faces_path = data_dir + '/Final/'

# Globals
dlib_get_face_detector = dlib.get_frontal_face_detector()
predict_shape = dlib.shape_predictor(data_dir + '/shape_predictor_68_face_landmarks.dat')
recognition_model = dlib.face_recognition_model_v1(data_dir + '/dlib_face_recognition_resnet_model_v1.dat')
face_classifier = cv2.CascadeClassifier(data_dir + '/haarcascade_frontalface_alt2.xml')

database_username_source = 'root213'
database_password_source = 'root213'
database_ip_source      = '192.168.10.137'
database_name_source     = 'employee_details'
database_connection_source = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username_source, database_password_source, 
                                                      database_ip_source, database_name_source))


def face_matches(trained_faces, face):
    b = np.linalg.norm(trained_faces - face, axis=1)
    #print("face_matches   : \n", a)
    return b


def find_match(trained_faces, trained_names, face):
    matches = face_matches(trained_faces, face) # get a list of True/False
    min_index = matches.argmin()
    min_value = matches[min_index]
        
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(relaypin, GPIO.OUT)
#     GPIO.output(relaypin, 1)
    
    if min_value < 0.43:
        
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(relaypin, GPIO.OUT)
#         GPIO.output(relaypin, 0)
#         GPIO.cleanup()
#         time.sleep(0.5)
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(relaypin, GPIO.OUT)
#         GPIO.output(relaypin, 1)
        return trained_names[min_index]#+" ({0:.2f})".format(min_value)
        
    if min_value < 0.50:
        #GPIO.output(relaypin, 1)
        return "Unknown"#+" ({0:.2f})".format(min_value)
    else:
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(relaypin, GPIO.OUT)
#         GPIO.output(relaypin, 0)
        return "Unknown"#+" ({0:.2f})".format(min_value)
    
def face_recognize_frame(trained_faces, trained_names):
    df = pd.read_csv("dataOFEmp.csv")
    fnl_Df = pd.read_csv("In Count Data2.csv")
##    df = pd.read_sql('SELECT * FROM employee_details.dataofemp;',con = database_connection_source)

    # Path to the video need to be detected.
    #cam = cv2.VideoCapture(data_dir + '/New folder/Skype_Video_2.mp4')

    # For Video cam Detection.
    cam = cv2.VideoCapture(0)
##    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
##    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 380)
    height = 720
    width = 380

    m = []
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        #start = datetime.now()
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        except:
            Ig = Image.open(frame).convert(L)
            gray = np.array(IG,"unit8")
        face_recognize = face_classifier.detectMultiScale(gray,scaleFactor=1.1,
                                                          minNeighbors=10,
                                                          flags=cv2.CASCADE_SCALE_IMAGE)# minSize=(220, 220),
                                                          #maxSize=(255, 255),
        
        #face_recognize = detector_dlib(frame)

        for (x, y, w, h) in face_recognize:
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            face = frame[y:y + h, x:x + w]
            layers = ([dlib.rectangle(left=0, top=0, right=w.item(), bottom=h.item())])  # int32 when opencv
            #layers = ([dlib_recgonize(w, h)])
            #start = datetime.now()
            faces_features = [predict_shape(face, face_layers) for face_layers in layers]
            face_encodes_image = [np.array(recognition_model.compute_face_descriptor(face, face_pose, 1)) for face_pose in faces_features]
            #face_encodes_image = face_encodes(face, layers)
            
#             matches = np.linalg.norm(trained_faces - face, axis=1) # get a list of True/False
#             min_index = matches.argmin()
#             min_value = matches[min_index]
            
            
            
            if (face_encodes_image):
                 match = find_match(trained_faces, trained_names, face_encodes_image[0])
                 if match != "Unknown" and match!= None:
                    m.append(match)
                    #print("length of m: ", len(m))
                 else:
                     pass 
                
                 if  len(m)>= 3 and match != "Unknown" and match!= None:
                     m = []
                     #print('welcome')
                     break
                 else:
                     pass
                
                 matchname = str(match)#.split(" ")
                
                #matchname = matchname[0]
                 if matchname.endswith("."):
                     matchname = matchname[:-1]

                #print(match)
                #print(matchname)
                 if type(matchname) == str and matchname != "Unknown":
                     #print(matchname)
                     a = df[df["Employee_Name"] == matchname]
                     #print(a)
                     a.index = [0]
                     a["shift_time"],a["DATE"],a["OUT TIME"],a["Day"] = "General",datetime.now().strftime("%d-%m-%Y"),datetime.now().strftime("%H:%M"), datetime.today().strftime('%A')
                     #a.to_sql(name='employee_out', con=database_connection_source, if_exists = 'append', index=False)
                     fnl_Df = pd.concat([fnl_Df,a],axis=0,join='outer',ignore_index=True)
                     fnl_Df.to_csv("In Count Data2.csv",index=False)
                
                     print("\n")
                     for each in a:
                         print(str(each) +":  ",a.loc[:,each][0])
                         #plt.imshow(image)
                 else:
                     continue
                 Emp_id = a["Employee_ID"][0]
                 cv2.putText(frame, str(Emp_id) +" : "+  matchname, (x+5, y-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.imshow("Face Recgnition", frame)
        if cv2.waitKey(1) == 27:
            break
    cam.release()
    cv2.destroyAllWindows()
    
    
    
dfn = pd.read_csv("face_marks1.csv")
##dfn = pd.read_sql('SELECT * FROM employee_details.face_marks;',con = database_connection_source)
nodal_points = []
for each in dfn["arrays"]:
    each = each[1:-1]
    a = np.fromstring(each, dtype=float, sep=' ')
    nodal_points.append(a)

names =  [each for each in dfn["Names"]]
names


face_recognize_frame(nodal_points,names)
