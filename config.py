class ConfigMain:
    LIBERATION_TIME_S = 30
    ENABLE_ARDUINO = False

class ConfigVideo:
    CAMERA_ID = 0
    CAPTURED_FRAME_WIDTH = 640
    CAPTURED_FRAME_HEIGHT = 480

class ConfigVideoFrame:
    class FaceRectangleColor:
        default = (255, 255, 255)
        liberated = (153, 255, 0)

    class FaceDetectionMethod:
        fastest = 'haarcascade'
        default = 'hog'
        precise = 'cnn'
    FACE_DETECTION_METHOD = FaceDetectionMethod.fastest

    MAX_FACES_DISTANCE = .5  # 0.0 to 1.0
    PROCESSED_FRAME_SHRINK_FACTOR = 2
    PROCESS_FACES_IN_EVERY_FRAME = True
    RECOGNIZE_FACES_EVERY_N_FRAME = 2
    UNKNOW_FACE_TEXT = 'Desconhecido'


class ConfigTempAccess:
    BASE_32_KEY = 'XCOBLUBMMAJND2GY'
    class QrCodeColor:
        default = (0, 255, 0)
        encrypted = (153, 255, 0)


class ConfigFacialId:
    DATASET_FILENAME = 'dataset.dat'

class ConfigArduino:
    USB_PATH: ''