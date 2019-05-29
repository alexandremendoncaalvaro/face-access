import face_recognition
import numpy as np
import pickle
from config import ConfigFacialId
from config import ConfigVideoFrame


class FacialIdDataset():
    def __init__(self):
        self.known_face_names = []
        self.known_face_encodings = []
        self.all_face_encodings = {}
        self.realtime_face_encodings = []
        self.realtime_face_names = []

    def load(self):
        try:
            with open(ConfigFacialId.DATASET_FILENAME, 'rb') as f:
                self.all_face_encodings = pickle.load(f)

            self.update()
        except:
            print(f'{ConfigFacialId.DATASET_FILENAME} file not found!')

    def add(self, name):
        self.load()
        face_saved = False
        while not face_saved:
            if len(self.realtime_face_encodings) > 0:
                if self.realtime_face_names[0] == ConfigVideoFrame.UNKNOW_FACE_TEXT:
                    self.all_face_encodings[name] = self.realtime_face_encodings[0]
                    self.save()
                    face_saved = True
    
    def addFromFile(self, name, image_path):
        loaded_image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(loaded_image)[0]
        self.all_face_encodings[name] = face_encoding
        self.save()

    def remove(self, to_remove):
        self.load()
        self.all_face_encodings.pop(to_remove, None)
        self.save()

    def update(self):
        self.known_face_names = list(
            self.all_face_encodings.keys())
        self.known_face_encodings = np.array(
            list(self.all_face_encodings.values()))

    def save(self):
        self.update()
        with open(ConfigFacialId.DATASET_FILENAME, 'wb') as f:
            pickle.dump(self.all_face_encodings, f)

    def print_names(self):
        print(self.known_face_names)
