import cv2
import dlib
import face_recognition
import numpy as np
from facial_id import *
from temp_access import *
from config import ConfigVideoFrame


facial_id_dataset = FacialIdDataset()
qr_code = QrCode()
otp = OneTimePassword()
haar_cascade_face = cv2.CascadeClassifier(
    'haarcascades/haarcascade_frontalface_alt2.xml')


class FrameFaces():
    locations = []
    encodings = []
    names = []
    images = []


class Frame():
    def __init__(self):
        self.current_non_processed_frame = 0
        self.are_there_recognized_faces = False
        self.face_rectangle_color = ConfigVideoFrame.FaceRectangleColor.default
        self.who_liberate = ''
        self.font = cv2.FONT_HERSHEY_DUPLEX
        self.font_size = 0.8


    def process_frame(self, frame):
        qr_codes, frame = qr_code.get_qr_codes(frame)
        self.get_faces(frame)
        painted_frame = self.paint_faces_rect(frame)
        return painted_frame

    def to_rgb_small_frame(self, frame):
        small_frame = cv2.resize(
            frame, (0, 0), fx=1/ConfigVideoFrame.PROCESSED_FRAME_SHRINK_FACTOR, fy=1/ConfigVideoFrame.PROCESSED_FRAME_SHRINK_FACTOR)
        rgb_small_frame = small_frame[:, :, ::-1]
        return rgb_small_frame

    def paint_faces_rect(self, frame):
        FrameFaces.images = []

        for (top, right, bottom, left), name in zip(FrameFaces.locations, FrameFaces.names):
            top *= ConfigVideoFrame.PROCESSED_FRAME_SHRINK_FACTOR
            right *= ConfigVideoFrame.PROCESSED_FRAME_SHRINK_FACTOR
            bottom *= ConfigVideoFrame.PROCESSED_FRAME_SHRINK_FACTOR
            left *= ConfigVideoFrame.PROCESSED_FRAME_SHRINK_FACTOR

            color = ConfigVideoFrame.FaceRectangleColor.default
            if self.who_liberate == name:
                color = self.face_rectangle_color

            cv2.rectangle(frame, (left, top),
                          (right, bottom), color, 2)
            cv2.putText(frame, name, (left + 1, bottom + 25),
                        self.font, self.font_size, color, 1)

        return frame

    def locate_faces(self, frame):
        rgb_small_frame = self.to_rgb_small_frame(frame)
        face_locations = []

        if ConfigVideoFrame.FACE_DETECTION_METHOD == ConfigVideoFrame.FaceDetectionMethod.fastest:
            gray_small_frame = cv2.cvtColor(
                rgb_small_frame, cv2.COLOR_BGR2GRAY)
            face_rect = haar_cascade_face.detectMultiScale(
                gray_small_frame, scaleFactor=1.2, minNeighbors=5)
            for (x, y, w, h) in face_rect:
                face_locations.append((y, x + w, y + h, x))
        else:
            face_locations = face_recognition.face_locations(
                rgb_small_frame, 1, ConfigVideoFrame.FACE_DETECTION_METHOD)

        FrameFaces.locations = face_locations
        FrameFaces.encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)


    def recognize_faces(self):
        face_names = []
        for face_encoding in FrameFaces.encodings:
            face_distances = face_recognition.face_distance(
                facial_id_dataset.known_face_encodings, face_encoding)
            name = ConfigVideoFrame.UNKNOW_FACE_TEXT
            for i, face_distance in enumerate(face_distances):
                if face_distance < ConfigVideoFrame.MAX_FACES_DISTANCE:
                    name = facial_id_dataset.known_face_names[i]
                    break
            face_names.append(name) 
        FrameFaces.names = face_names
        recognized_faces = [x for x in face_names if x != ConfigVideoFrame.UNKNOW_FACE_TEXT]
        self.are_there_recognized_faces = len(recognized_faces) > 0
        if self.are_there_recognized_faces:
            self.who_liberate = recognized_faces[0]
        facial_id_dataset.realtime_face_encodings = FrameFaces.encodings
        facial_id_dataset.realtime_face_names = FrameFaces.names
        

    def get_faces(self, frame):
        if ConfigVideoFrame.PROCESS_FACES_IN_EVERY_FRAME:
            self.locate_faces(frame)
            self.recognize_faces()
        else:
            self.current_non_processed_frame += 1
            should_process_this_frame = self.current_non_processed_frame >= ConfigVideoFrame.RECOGNIZE_FACES_EVERY_N_FRAME
            if should_process_this_frame:
                self.current_non_processed_frame = 0
                self.locate_faces(frame)
                self.recognize_faces()
