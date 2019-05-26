import face_recognition
import numpy as np
import pickle
from config import ConfigFacialId


class FacialIdDataset():
    def __init__(self):
        self.known_face_names = []
        self.known_face_encodings = []
        self.all_face_encodings = {}
        self.realtime_face_encodings = []

    def load(self):
        try:
            with open(ConfigFacialId.DATASET_FILENAME, 'rb') as f:
                self.all_face_encodings = pickle.load(f)

            self.update()
        except:
            print(f'{ConfigFacialId.DATASET_FILENAME} file not found!')

    def add(self, name):
        self.load()
        realtime_face_encoding = self.realtime_face_encodings[0]
        self.all_face_encodings[name] = realtime_face_encoding
        self.save()
    
    def addFromFile(self, name, image_path):
        loaded_image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(loaded_image)[0]
        self.all_face_encodings[name] = face_encoding
        self.save()

    def remove(self, to_remove):
        self.load()
        self.all_face_encodings.pop(to_remove)
        self.save()

    def update(self):
        self.known_face_names = list(
            self.all_face_encodings.keys())
        self.known_face_encodings = np.array(
            list(self.all_face_encodings.values()))

    def save(self):
        self.update()
        with open(config.DATASET_FILENAME, 'wb') as f:
            pickle.dump(self.all_face_encodings, f)

    def print_names(self):
        print(self.known_face_names)
