import threading
from video import Image, Video
from video_frame import *

video = Video()
image = Image()
video_frame = Frame()

def main():
    video_frame.load_facial_ids()

    thread_cli = threading.Thread(target=execute_cli)
    thread_cli.start()

    loop = True
    while loop:
        frame = video.get_frame()
        processed_frame = video_frame.process_frame(frame)

        video.update_window(processed_frame)

        loop = video.stop_when_key_press('q')
        if not thread_cli.isAlive():
            loop = False

    video.finish()


def execute_command(command):
    loop = True
    commands = command.split(',')
    if command == 'update' or command == 'refresh':
        video_frame.load_facial_ids()
    elif command == 'exit' or command == 'quit' or command == 'q':
        loop = False
    elif command == 'print' or command == 'faces' or command == 'names' or command == 'ids':
        facial_id.print_names()
    elif command.find('add') > -1:
        total_parameters = len(commands)-1
        name = commands[1]
        if total_parameters > 1:
            image_path = commands[total_parameters]
        else:
            video_frame.save_current_face()
            image_path = 'face_image.jpg'
        facial_id.add(name, image_path)
        facial_id.print_names()
        video_frame.load_facial_ids()
    elif command.find('del') > -1 or command.find('rem') > -1:
        name = commands[1]
        facial_id.remove(name)
        facial_id.print_names()
        video_frame.load_facial_ids()
    else:
        print('Comando não identificado!')

    return loop


def execute_cli():
    loop = True
    while loop:
        command = input("CMD: ")
        loop = execute_command(command)


main()
