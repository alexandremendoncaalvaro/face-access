import threading
import time
from video import Image, Video
from video_frame import *

LIBERATION_TIME_S = 30

video = Video()
image = Image()
video_frame = Frame()


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
        command = input('CMD: ')
        keep_looping = execute_command(command)


thread_cli = threading.Thread(target=looping_cli)


def execute_command(command):
    keep_looping = True
    commands = command.split(',')

    if command in ['update', 'refresh']:
        facial_id_dataset.load()

    elif command in ['exit', 'quit', 'q']:
        keep_looping = False

    elif command in ['print', 'faces', 'names', 'ids']:
        facial_id_dataset.print_names()

    elif command[:3] == 'add':
        total_parameters = len(commands)-1
        name = commands[1]

        # add,firstname lastname,file.jpg
        if total_parameters == 2:
            face_image = commands[2]
            facial_id_dataset.addFromFile(name, face_image)
        # add,firstname lastname
        elif total_parameters == 1:
            facial_id_dataset.add(name)

        facial_id_dataset.print_names()

    elif command[:3] == 'del' or command[:3] == 'rem':
        name = commands[1]
        facial_id_dataset.remove(name)
        facial_id_dataset.print_names()

    elif command in ['generate key']:
        result = otp.get_new_base32_key()
        print(result)

    elif command[:8] == 'password':
        key = commands[1]
        result = otp.verify(key)
        if result:
            give_access()
        else:
            print('Chave inválida!')

    elif command[:7] == 'encrypt':
        message = command[1]

    elif command == '':
        pass

    else:
        print('Comando não identificado!')

    return keep_looping


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


thread_grant_access = threading.Thread(target=grant_access)


def give_access():
    global thread_grant_access
    if not thread_grant_access.is_alive():
        thread_grant_access = threading.Thread(target=grant_access)
        thread_grant_access.start()


if __name__ == '__main__':
    main()
