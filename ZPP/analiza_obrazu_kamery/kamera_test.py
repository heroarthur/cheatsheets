#!/usr/bin/python3
import cv2
import numpy as np
import face_video_detectors as fvd 

class faceCascadeArgs:
    def __init__(self, scaleFactor=1.1, minNeighbors=5,minSize=(20,20),flags=cv2.CASCADE_SCALE_IMAGE):
        self.scaleFactor = scaleFactor,
        self.minNeighbors = minNeighbors,
        self.minSize = minSize,
        self.flags = flags

update_frequency = 10
shape5_predictor_path = "models/shape_predictor_5_face_landmarks.dat"
shape68_predictor_path = "models/shape_predictor_68_face_landmarks.dat"
faceCascade_xml = "models/haarcascade_frontalface_default.xml"
faceCascade_arguments = faceCascadeArgs()



testowe_video = 'family_short_360.mp4'

cap = cv2.VideoCapture(testowe_video)
face_detectors = fvd.detectors(update_frequency, faceCascade_arguments, faceCascade_xml, shape68_predictor_path, shape5_predictor_path, faceCascade_xml)
 

# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video stream or file")
 
# Read until video is completed
while(cap.isOpened()):
    ret, frame = cap.read() #Capture frame-by-frame
    if ret == False:
        break
        
    marked_faces = face_detectors.update_detections(frame)
    face_detectors.print_detection_log()

    cv2.imshow('Frame',marked_faces) # Display the resulting frame
    
    if cv2.waitKey(25) == ord('q'): 
        break
     


cap.release()
cv2.destroyAllWindows() #close all Hight GUI objects