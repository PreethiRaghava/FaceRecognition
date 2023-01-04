import os
import dlib
from PIL import Image
import numpy as np
from skimage import io
import cv2
from datetime import datetime
import pandas as pd 
##from sqlalchemy import create_engine
##import pymysql
import random
import time
import sqlalchemy
#import RPi.GPIO as GPIO

work_dir = os.getcwd()
data_dir = os.path.expanduser(work_dir)
faces_path = data_dir + '/Final_Images/'

# Globals
dlib_get_face_detector = dlib.get_frontal_face_detector()
predict_shape = dlib.shape_predictor(data_dir + '/shape_predictor_68_face_landmarks.dat')
recognition_model = dlib.face_recognition_model_v1(data_dir + '/dlib_face_recognition_resnet_model_v1.dat')
                                

def load_face_encodes(faces_path):
    image_names = filter(lambda x:(x.endswith('.jpg') or x.endswith('.png') or x.endswith('.jpeg') or x.endswith('.PNG') or x.endswith('.JPG')), os.listdir(faces_path))
    image_names = sorted(image_names)
    for each in image_names:
        #print(each)
        if each.endswith('.jpg') or each.endswith('.png') or each.endswith('.PNG') or each.endswith('.JPG'):
            trained_names = [x[:-4] for x in image_names]
        elif each.endswith('.jpeg') or each.endswith(".JPEG"):
            trained_names = [x[:-5] for x in image_names]
    #print(image_names)
    #print(image_names)
     
    images_paths = [faces_path + x for x in image_names]
    trained_faces = []

    win = dlib.image_window()

    for image_path in images_paths:
        face = io.imread(image_path)

        faces_layers = dlib_get_face_detector(face, 0)
##
##        if len(faces_layers) != 1:
##            print("Expected one and only one face per image: " + image_path + " - it has " + str(len(faces_layers)))
##            exit()

        face_layers = faces_layers[0]
        face_features = predict_shape(face, face_layers)
        face_encode = np.array(recognition_model.compute_face_descriptor(face, face_features, 0))

        win.clear_overlay()
        win.set_image(face)
        win.add_overlay(face_layers)
        win.add_overlay(face_features)
        trained_faces.append(face_encode)
    return trained_faces, trained_names

trained_faces, trained_names = load_face_encodes(faces_path)

face_df = pd.DataFrame()
face_df["arrays"] = trained_faces
face_df["Names"] = trained_names

face_df.to_csv("SPsoft_face_marks.csv",index = False)

nodal_points = []
for each in face_df["arrays"]:
    each = each[1:-1]
    a = np.fromstring(each, dtype=float, sep=' ')
    nodal_points.append(a)

names =  [each for each in face_df["Names"]]
names
##face_df.to_json("face_marks_json1.json")
