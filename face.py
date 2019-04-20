import face_recognition
import cv2
import numpy as np
import pickle
import glob
from video import Image

MAX_FACE_DISTANCE = .4
PROCESSED_FRAME_SHRINK_FACTOR = 5
RECOGNIZE_EVERY_N_FRAME = 10


class Face:
    _current_non_processed_frame = 0
    _face_locations = []

    _face_encodings = []
    _face_names = []

    _known_face_names = []
    _known_face_encodings = []

    _faces_images = []

    def load_facial_ids():
        with open('dataset_faces.dat', 'rb') as f:
            all_face_encodings = pickle.load(f)
        Face._known_face_names = list(all_face_encodings.keys())
        Face._known_face_encodings = np.array(
            list(all_face_encodings.values()))

    def process_frame(frame):
        Face.process_faces(frame)
        painted_frame = Face.paint_frame(frame)
        return painted_frame

    def to_rgb_small_frame(frame):
        small_frame = cv2.resize(
            frame, (0, 0), fx=1/PROCESSED_FRAME_SHRINK_FACTOR, fy=1/PROCESSED_FRAME_SHRINK_FACTOR)
        rgb_small_frame = small_frame[:, :, ::-1]
        return rgb_small_frame

    def paint_frame(frame):
        font = cv2.FONT_HERSHEY_DUPLEX
        font_size = 0.8

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        Face._faces_images = []

        for (top, right, bottom, left), name in zip(Face._face_locations, Face._face_names):
            top *= PROCESSED_FRAME_SHRINK_FACTOR
            right *= PROCESSED_FRAME_SHRINK_FACTOR
            bottom *= PROCESSED_FRAME_SHRINK_FACTOR
            left *= PROCESSED_FRAME_SHRINK_FACTOR

            face_image = frame[top:bottom, left:right]
            Face._faces_images.append(face_image)

            cv2.rectangle(frame, (left, top),
                          (right, bottom), (255, 255, 255), 2)
            cv2.putText(frame, name, (left + 1, bottom + 25),
                        font, font_size, (255, 255, 255), 1)
       
        return frame
        
    def get_faces_images():
        return Face._faces_images

    def locate_faces(frame):
        rgb_small_frame = Face.to_rgb_small_frame(frame)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        Face._face_locations = face_locations
        Face._face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

    def recognize_faces():
        face_names = []
        for face_encoding in Face._face_encodings:
            face_distances = face_recognition.face_distance(
                Face._known_face_encodings, face_encoding)
            name = "Desconhecido"
            for i, face_distance in enumerate(face_distances):
                if face_distance < MAX_FACE_DISTANCE:
                    name = Face._known_face_names[i]
                    break
            face_names.append(name)
        Face._face_names = face_names

    def process_faces(frame):
        Face.locate_faces(frame)
        Face._current_non_processed_frame += 1
        should_process_this_frame = Face._current_non_processed_frame >= RECOGNIZE_EVERY_N_FRAME

        if should_process_this_frame:
            Face._current_non_processed_frame = 0
            Face.recognize_faces()
