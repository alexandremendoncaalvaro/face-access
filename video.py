import cv2
import face_recognition
import numpy as np

class Image():
    def verify_alpha_channel(self, frame):
        try:
            frame.shape[3]  # looking for the alpha channel
        except IndexError:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        return frame

    def apply_color_overlay(self, frame, intensity=0.5, blue=0, green=0, red=0):
        frame = self.verify_alpha_channel(frame)
        frame_h, frame_w, frame_c = frame.shape
        sepia_bgra = (blue, green, red, 1)
        overlay = np.full((frame_h, frame_w, 4), sepia_bgra, dtype='uint8')
        cv2.addWeighted(overlay, intensity, frame, 1.0, 0, frame)
        return frame

class Video():
    def __init__(self):
        self._video_capture = cv2.VideoCapture(0)

    def get_frame(self):
        ret, frame = self._video_capture.read()
        return frame

    def update_window(self, frame):
        cv2.imshow('Video', frame)
   
    def stop_when_key_press(self, key):
        stop = False
        if cv2.waitKey(1) & 0xFF == ord(key):
            stop = True
        return stop

    def finish(self):
        self._video_capture.release()
        cv2.destroyAllWindows()
