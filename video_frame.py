import cv2
import face_recognition
from facial_id import *
from temp_access import *

MAX_FACE_DISTANCE = .4
PROCESSED_FRAME_SHRINK_FACTOR = 5
RECOGNIZE_EVERY_N_FRAME = 10
UNKNOW_FACE_TEXT = 'Desconhecido'
TEMP_FACE_IMAGE_FILENAME = 'face_image.jpg'

facial_id_dataset = FacialIdDataset()
qr_code = QrCode()

class FrameFaces():
    locations = []
    encodings = []
    names = []
    images = []

class Frame():
    def __init__(self):
        self.current_non_processed_frame = 0
        self.are_there_recognized_faces = False

    def process_frame(self, frame):
        qr_codes, frame = qr_code.get_qr_codes(frame)
        self.process_faces(frame)
        painted_frame = self.paint_faces_rect(frame)
        return painted_frame

    def to_rgb_small_frame(self, frame):
        small_frame = cv2.resize(
            frame, (0, 0), fx=1/PROCESSED_FRAME_SHRINK_FACTOR, fy=1/PROCESSED_FRAME_SHRINK_FACTOR)
        rgb_small_frame = small_frame[:, :, ::-1]
        return rgb_small_frame

    def paint_faces_rect(self, frame):
        font = cv2.FONT_HERSHEY_DUPLEX
        font_size = 0.8

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        FrameFaces.images = []

        for (top, right, bottom, left), name in zip(FrameFaces.locations, FrameFaces.names):
            top *= PROCESSED_FRAME_SHRINK_FACTOR
            right *= PROCESSED_FRAME_SHRINK_FACTOR
            bottom *= PROCESSED_FRAME_SHRINK_FACTOR
            left *= PROCESSED_FRAME_SHRINK_FACTOR

            face_image = frame[top:bottom, left:right]
            FrameFaces.images.append(face_image)

            cv2.rectangle(frame, (left, top),
                          (right, bottom), (255, 255, 255), 2)
            cv2.putText(frame, name, (left + 1, bottom + 25),
                        font, font_size, (255, 255, 255), 1)

        return frame


    def save_current_face(self):
        try_again = True
        while try_again:
            try:
                if len(FrameFaces.images) > 0:
                    cv2.imwrite(TEMP_FACE_IMAGE_FILENAME,
                                FrameFaces.images[0])
                try_again = False
            except:
                try_again = True

    def locate_faces(self, frame):
        rgb_small_frame = self.to_rgb_small_frame(frame)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        FrameFaces.locations = face_locations
        FrameFaces.encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

    def recognize_faces(self):
        face_names = []
        for face_encoding in FrameFaces.encodings:
            face_distances = face_recognition.face_distance(
                facial_id_dataset.known_face_encodings, face_encoding)
            name = UNKNOW_FACE_TEXT
            for i, face_distance in enumerate(face_distances):
                if face_distance < MAX_FACE_DISTANCE:
                    name = facial_id_dataset.known_face_names[i]

                    break
            face_names.append(name)
        FrameFaces.names = face_names
        recognized_faces = [x for x in face_names if x != "Desconhecido"]
        self.are_there_recognized_faces = len(recognized_faces) > 0

    def process_faces(self, frame):
        self.locate_faces(frame)

        self.current_non_processed_frame += 1

        should_process_this_frame = self.current_non_processed_frame >= RECOGNIZE_EVERY_N_FRAME
        if should_process_this_frame:
            self.current_non_processed_frame = 0
            self.recognize_faces()
