import sys
import face_recognition
import cv2
import numpy as np
import pickle
import glob

DATASET_FILENAME = 'dataset.dat'

class FacialId():
    def __init__(self):
        self.known_face_names = []
        self.known_face_encodings = []
        self.all_face_encodings = {}

    def load(self):
        try:
            with open(DATASET_FILENAME, 'rb') as f:
                self.all_face_encodings = pickle.load(f)

            self.known_face_names = list(
                self.all_face_encodings.keys())
            self.known_face_encodings = np.array(
                list(self.all_face_encodings.values()))
        except:
            print('Dataset file not found!')
        

    def add(self, name, image_path):
        self.load()
        loaded_image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(loaded_image)[0]
        self.all_face_encodings[name] = face_encoding
        self.known_face_names = list(
            self.all_face_encodings.keys())
        with open(DATASET_FILENAME, 'wb') as f:
            pickle.dump(self.all_face_encodings, f)

    def remove(self, to_remove):
        self.load()
        self.all_face_encodings.pop(to_remove)
        self.known_face_names = list(
            self.all_face_encodings.keys())
        with open(DATASET_FILENAME, 'wb') as f:
            pickle.dump(self.all_face_encodings, f)

    def print_names(self):
        print(self.known_face_names)


# facial_id = FacialId()
# total_arguments = len(sys.argv)

# if total_arguments == 3:
#     name = sys.argv[1]
#     image_path = sys.argv[2]
#     facial_id.add(name, image_path)
# elif total_arguments == 2:
#     to_remove = sys.argv[1]
#     facial_id.remove(to_remove)
# elif total_arguments == 1:
#     facial_id.load()

# facial_id.print_names()