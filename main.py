import threading
import time
from video import Image, Video
from video_frame import *


def main():
    setup()
    video_loop()
    video.finish()


def setup():
    facial_id_dataset.load()
    thread_cli.start()


def video_loop():
    while True:
        frame = video.get_frame()
        processed_frame = video_frame.process_frame(frame)
        if video_frame.are_there_recognized_faces:
            give_access()

        video.update_window(processed_frame)

        if video.stop_when_key_press('q'):
            break
        if not thread_cli.is_alive():
            break


def cli_loop():
    while True:
        command = input("CMD: ")
        keep_looping = execute_command(command)
        if not keep_looping:
            break


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

    else:
        print('Comando não identificado!')

    return keep_looping


def add_face_from_file_path(commands):
    return commands[2]


def add_face_from_current_frame():
    video_frame.save_current_face()
    image_path = 'face_image.jpg'
    return image_path

def give_access():
    global thread_grant_access
    if not thread_grant_access.is_alive():
        thread_grant_access = threading.Thread(target=grant_access)
        thread_grant_access.start()

def grant_access():
    print('Acesso liberado!')
    time.sleep(10)

video = Video()
image = Image()
video_frame = Frame()
thread_cli = threading.Thread(target=cli_loop)
thread_grant_access = threading.Thread(target=grant_access)
main()
