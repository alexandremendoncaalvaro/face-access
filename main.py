import threading
import time
from video import *
from face import *
from facial_id import FacialId

def execute_command(command):
    loop = True
    try:
        commands = command.split(',')
        if command == 'update' or command == 'refresh':
            Face.load_facial_ids()
        elif command == 'exit' or command == 'quit' or command == 'q':
            loop = False
        elif command == 'print' or command == 'faces' or command == 'names' or command == 'ids':
            FacialId.print_names()
        elif command.find('add') > -1:
            total_parameters = len(commands)-1
            name = commands[1]
            if total_parameters > 1:
                image_path = commands[total_parameters]
            else:
                save_current_face()
                image_path = 'face_image.jpg'
            FacialId.add(name, image_path)
            FacialId.print_names()
            Face.load_facial_ids()
        elif command.find('del') > -1 or command.find('rem') > -1 :
            name = commands[1]
            FacialId.remove(name)
            FacialId.print_names()
            Face.load_facial_ids()
        else:
            print('Comando não identificado!')

    except EnvironmentError:
        print('Erro ao tentar executar o comando!')
    
    return loop


def save_current_face():
    loop = True
    while loop:
        faces_images = Face.get_faces_images()
        if len(faces_images) > 0:
            cv2.imwrite('face_image.jpg', faces_images[0])
            loop = False


def update_database():
    loop = True
    while loop:
        command = input("CMD: ")
        loop = execute_command(command)


def do_frame_actions(frame):
    processed_frame = Face.process_frame(frame)
    return processed_frame


t = threading.Thread(target=update_database)
t.start()

Face.load_facial_ids()

still_playing = True

while still_playing:
    frame = Video.get_frame()
    updated_frame = do_frame_actions(frame)
    Video.update_window(updated_frame)
    still_playing = Video.stop_when_key_press('q')
    if not t.isAlive():
        still_playing = False

Video.finish()
