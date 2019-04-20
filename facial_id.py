import sys
import face_recognition
import cv2
import numpy as np
import pickle
import glob

class FacialId:
    _known_face_names = []
    _known_face_encodings = []
    _all_face_encodings = {}

    def load():
        with open('dataset_faces.dat', 'rb') as f:
            FacialId._all_face_encodings = pickle.load(f)

        FacialId._known_face_names = list(
            FacialId._all_face_encodings.keys())
        FacialId._known_face_encodings = np.array(
            list(FacialId._all_face_encodings.values()))

    def add(name, image_path):
        FacialId.load()
        loaded_image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(loaded_image)[0]
        FacialId._all_face_encodings[name] = face_encoding
        FacialId._known_face_names = list(
            FacialId._all_face_encodings.keys())
        with open('dataset_faces.dat', 'wb') as f:
            pickle.dump(FacialId._all_face_encodings, f)

    def remove(to_remove):
        FacialId.load()
        FacialId._all_face_encodings.pop(to_remove)
        FacialId._known_face_names = list(
            FacialId._all_face_encodings.keys())
        with open('dataset_faces.dat', 'wb') as f:
            pickle.dump(FacialId._all_face_encodings, f)

    def print_names():
        print(FacialId._known_face_names)


total_arguments = len(sys.argv)

if total_arguments == 3:
    name = sys.argv[1]
    image_path = sys.argv[2]
    FacialId.add(name, image_path)
elif total_arguments == 2:
    to_remove = sys.argv[1]
    FacialId.remove(to_remove)
elif total_arguments == 1:
    FacialId.load()

FacialId.print_names()
