import threading
import time
from video import Image, Video
from video_frame import *

LIBERATION_TIME_S = 30


def main():
    setup()
    looping_video()
    video.finish()


def setup():
    facial_id_dataset.load()
    thread_cli.start()


def looping_video():
    keep_looping = True
    while keep_looping:
        frame = video.get_frame()
        processed_frame = video_frame.process_frame(frame)
        if video_frame.are_there_recognized_faces:
            give_access()

        video.update_window(processed_frame)
        keep_looping = thread_cli.is_alive() and not video.stop_when_key_press('q')


def looping_cli():
    keep_looping = True
    while keep_looping:
        command = input("CMD: ")
        keep_looping = execute_command(command)


def execute_command(command):
    keep_looping = True
    commands = command.split(',')

    if command in ['update', 'refresh']:
        facial_id_dataset.load()

    elif command in ['exit', 'quit', 'q']:
        keep_looping = False

    elif command in ['print', 'faces', 'names', 'ids']:
        facial_id_dataset.print_names()

    elif command.find('add') > -1:
        total_parameters = len(commands)-1

        name = commands[1]

        # add,firstname lastname,file.jpg
        if total_parameters == 2:
            face_image = add_face_from_file_path(commands)

        # add,firstname lastname
        elif total_parameters == 1:
            face_image = add_face_from_current_frame()

        facial_id_dataset.add(name, face_image)
        facial_id_dataset.print_names()

    elif command.find('del') > -1 or command.find('rem') > -1:
        name = commands[1]
        facial_id_dataset.remove(name)
        facial_id_dataset.print_names()

    elif command in ['generate key']:
        result = otp.get_new_base32_key()
        print(result)

    elif command.find('password') > -1:
        key = commands[1]
        result = otp.verify(key)
        if result:
            give_access()
        else:
            print('Chave inválida!')

    elif command.find('encrypt') > -1:
        message = command[1]
        cipher = crypt.encrypt_message(message)
        print(cipher)
        result = crypt.decrypt_message(cipher)
        print(result)

    elif command == '':
        pass

    else:
        print('Comando não identificado!')

    return keep_looping


def add_face_from_file_path(commands):
    return commands[2]


def add_face_from_current_frame():
    video_frame.save_current_face()
    image_path = TEMP_FACE_IMAGE_FILENAME
    return image_path


def give_access():
    global thread_grant_access
    if not thread_grant_access.is_alive():
        thread_grant_access = threading.Thread(target=grant_access)
        thread_grant_access.start()


def grant_access():
    print()
    print('Acesso liberado!')
    print()
    print('CMD: ', end='', flush=True)
    video_frame.face_rectangle_color = FaceRectangleColor.liberated
    global thread_cli
    end_access_time = time.time() + LIBERATION_TIME_S
    still_wait = True
    while still_wait:
        liberation_finished = time.time() >= end_access_time
        if not thread_cli.is_alive() or liberation_finished:
            still_wait = False
    video_frame.face_rectangle_color = FaceRectangleColor.default
    video_frame.who_liberate = ''



video = Video()
image = Image()
video_frame = Frame()
thread_cli = threading.Thread(target=looping_cli)
thread_grant_access = threading.Thread(target=grant_access)
main()
