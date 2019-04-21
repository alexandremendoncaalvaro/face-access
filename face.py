import face_recognition
import cv2
from facial_id import *


MAX_FACE_DISTANCE = .4
PROCESSED_FRAME_SHRINK_FACTOR = 5
RECOGNIZE_EVERY_N_FRAME = 10
UNKNOW_FACE_TEXT = 'Desconhecido'
TEMP_FACE_IMAGE_FILENAME = 'face_image.jpg'

facial_id = FacialId()


class Face():
    def __init__(self):
        self._current_non_processed_frame = 0
        self._face_locations = []
        self._face_encodings = []
        self._face_names = []
        self._faces_images = []

    def load_facial_ids(self):
        facial_id.load()

    def process_frame(self, frame):
        self.process_faces(frame)
        painted_frame = self.paint_frame(frame)
        return painted_frame

    def to_rgb_small_frame(self, frame):
        small_frame = cv2.resize(
            frame, (0, 0), fx=1/PROCESSED_FRAME_SHRINK_FACTOR, fy=1/PROCESSED_FRAME_SHRINK_FACTOR)
        rgb_small_frame = small_frame[:, :, ::-1]
        return rgb_small_frame

    def paint_frame(self, frame):
        font = cv2.FONT_HERSHEY_DUPLEX
        font_size = 0.8

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        self._faces_images = []

        for (top, right, bottom, left), name in zip(self._face_locations, self._face_names):
            top *= PROCESSED_FRAME_SHRINK_FACTOR
            right *= PROCESSED_FRAME_SHRINK_FACTOR
            bottom *= PROCESSED_FRAME_SHRINK_FACTOR
            left *= PROCESSED_FRAME_SHRINK_FACTOR

            face_image = frame[top:bottom, left:right]
            self._faces_images.append(face_image)

            cv2.rectangle(frame, (left, top),
                          (right, bottom), (255, 255, 255), 2)
            cv2.putText(frame, name, (left + 1, bottom + 25),
                        font, font_size, (255, 255, 255), 1)

        return frame

    def get_faces_images(self):
        return self._faces_images

    def save_current_face(self):
        try_again = True
        while try_again:
            try:
                if len(self._faces_images) > 0:
                    cv2.imwrite(TEMP_FACE_IMAGE_FILENAME,
                                self._faces_images[0])
                try_again = False
            except:
                try_again = True

    def locate_faces(self, frame):
        rgb_small_frame = self.to_rgb_small_frame(frame)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        self._face_locations = face_locations
        self._face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

    def recognize_faces(self):
        face_names = []
        for face_encoding in self._face_encodings:
            face_distances = face_recognition.face_distance(
                facial_id.known_face_encodings, face_encoding)
            name = UNKNOW_FACE_TEXT
            for i, face_distance in enumerate(face_distances):
                if face_distance < MAX_FACE_DISTANCE:
                    name = facial_id.known_face_names[i]
                    break
            face_names.append(name)
        self._face_names = face_names

    def process_faces(self, frame):
        self.locate_faces(frame)
        self._current_non_processed_frame += 1
        should_process_this_frame = self._current_non_processed_frame >= RECOGNIZE_EVERY_N_FRAME

        if should_process_this_frame:
            self._current_non_processed_frame = 0
            self.recognize_faces()
