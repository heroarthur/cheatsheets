#!/usr/bin/python3
import cv2
import numpy as np
import dlib
import time
import os


red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)



def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def dlib_shape2list(shape):
    return [(shape.part(i).x, shape.part(i).y) for i in range(shape.num_parts)]

#detections for different models
def landmark_points_detection(landmark_predictor_model, frame, face_rec_dets):
    points_lists = []
    for k, d in enumerate(face_rec_dets):
        shape = landmark_predictor_model(frame, d)
        points_lists.append(dlib_shape2list(shape))
    return points_lists

def opencv_haarcascade_detection(image, faceCascade_classifier, faceCascade_arguments):
    fca = faceCascade_arguments
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade_classifier.detectMultiScale(
		gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(20, 20),
        flags = cv2.CASCADE_SCALE_IMAGE
	)
    return faces


#marking detection on image
def mark_image_faces(img, dets, arr = np.array([255,255,255])):
    marked_img = img
    for d in dets:
        top = d.top(); bottom = d.bottom(); left = d.left(); right = d.right();
        thick = 5
        marked_col = list(range(left,(left+thick)))+list(range((right-thick),right))
        marked_row = list(range(top,(top+thick)))+list(range((bottom-thick),bottom))
        marked_img[top:bottom , marked_col] = arr
        marked_img[marked_row , left:right] = arr
    return marked_img

def mark_landmark_points(img, points_lists, rad=3, color=blue):
    fill_circle = -1
    for l in points_lists:
        for point in l:
            cv2.circle(img, point, rad, color, fill_circle)

def draw_rectangles(img, det_faces, color=green):
    for (x, y, w, h) in det_faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)


class detectors:
    def __init__(self, update_detection_frequency, faceCascade_arguments, casc_classifier_path, shape_68_face_landmarks_path, shape_5_face_landmarks_path, haarcascade_frontalface_xml_path):
        self.update_detection_frequency = update_detection_frequency
        self.frames_counter = 0
        self.detected_faces = 0
        self.last_detection_time = 0

        self.shape68predictor = dlib.shape_predictor(shape_68_face_landmarks_path)
        self.shape5predictor = dlib.shape_predictor(shape_5_face_landmarks_path)
        self.faceCascade = cv2.CascadeClassifier(haarcascade_frontalface_xml_path)

        self.dlib_face_detector = dlib.get_frontal_face_detector()
        self.detections = {'dlib': [], 'landmark5': [], 'landmark68': [], 'opencv_haarcascade': []}

        self.faceCascade_arguments = faceCascade_arguments
        self.faceCascade_classifier = cv2.CascadeClassifier(casc_classifier_path)



    def should_update_detection(self):
        return self.frames_counter % self.update_detection_frequency == 0 or \
               self.last_detection_time == 0

    def make_detections(self, frame):
        self.last_detection_time = time.time()
        self.detections['dlib'] = self.dlib_face_detector(frame, 1)
        self.detections['landmark5'] = landmark_points_detection(self.shape5predictor, frame, self.detections['dlib'])
        self.detections['landmark68'] = landmark_points_detection(self.shape68predictor, frame, self.detections['dlib'])
        self.detections['opencv_haarcascade'] = opencv_haarcascade_detection(frame, self.faceCascade_classifier, self.faceCascade_arguments)

        

    def update_detections(self, frame):
        self.frames_counter += 1
        if self.should_update_detection():
            self.make_detections(frame)
        #drawing points and rectangles for all detections by all models
        mark_image_faces(frame, self.detections['dlib'])
        mark_landmark_points(frame, self.detections['landmark68'])
        mark_landmark_points(frame, self.detections['landmark5'], color=yellow)
        draw_rectangles(frame, self.detections['opencv_haarcascade'])
        return frame
        #mark_landmark_points

    def print_detection_log(self):
        clear_console()
        try: 
            print("det. time: {}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.last_detection_time))))
            print("dlib det. faces: {}".format(len(self.detections['dlib'])))
            print("opencv2 det. faces: {}".format(len(self.detections['opencv_haarcascade'])))
        except:
            print("det. faces: 0")


            