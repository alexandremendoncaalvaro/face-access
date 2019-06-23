import threading
import time
from video import Image, Video
from video_frame import *
from arduino import ArduinoBoard
from config import ConfigMain


keep_loopings = True
background_command = ''

video = Video()
image = Image()
video_frame = Frame()
arduino_board = ArduinoBoard() if ConfigMain.ENABLE_ARDUINO else None

def main():
    setup()
    looping_video()
    video.finish()


def setup():
    facial_id_dataset.load()
    thread_cli.start()
    thread_background_command.start()


def looping_cli():
    global keep_loopings
    while keep_loopings:
        command = input('CMD: ')
        keep_loopings = execute_command(command)


def looping_background_command():
    global background_command, keep_loopings
    while keep_loopings:
        if background_command != '':
            print(background_command)
            keep_loopings = execute_command(background_command)
            background_command = ''


def looping_video():
    keep_looping = True
    while keep_looping:
        frame = video.get_frame()
        valid_qrcode, processed_frame = video_frame.process_frame(frame)
        if valid_qrcode != '':
            global background_command
            background_command = f'add,{valid_qrcode}'
        if video_frame.are_there_recognized_faces:
            give_access()

        video.update_window(processed_frame)
        keep_looping = thread_cli.is_alive() and not video.stop_when_key_press('q')


def execute_command(command):
    keep_looping = True
    try:
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
            otp_key = otp.get_new_base32_key()
            print(f'OTP key: {otp_key}')
            crypto_key = crypto.get_key()
            print(f'Cryptography key: {crypto_key}')

        elif command[:8] == 'password':
            key = commands[1]
            otp_key = otp.verify(key)
            if otp_key:
                give_access()
            else:
                print('Chave inválida!')

        elif command[:7] == 'encrypt':
            message = commands[1]
            result = crypto.encrypt(message)
            print(result.decode('utf-8'))

        elif command[:7] == 'decrypt':
            message = commands[1]
            result = crypto.decrypt(message)
            print(result.decode('utf-8'))

        elif command[:2] == 'qr':
            message = commands[1]
            print('Gerando QR-Code criptografado na pasta qrcodes...')
            result = qr_code.generate(message)

        elif command == '':
            pass

        else:
            print('Comando não identificado!')
    except:
        print('Comando inválido!')

    return keep_looping


def grant_access():
    print()
    print('Acesso liberado!')
    print()
    print('CMD: ', end='', flush=True)
    if arduino_board != None:
        arduino_board.set_relay(1)
    video_frame.face_rectangle_color = ConfigVideoFrame.FaceRectangleColor.liberated
    global thread_cli
    end_access_time = time.time() + ConfigMain.LIBERATION_TIME_S
    still_wait = True
    while still_wait:
        liberation_finished = time.time() >= end_access_time
        if not thread_cli.is_alive() or liberation_finished:
            still_wait = False
    if arduino_board != None:
        arduino_board.set_relay(0)
    video_frame.face_rectangle_color = ConfigVideoFrame.FaceRectangleColor.default
    video_frame.who_liberate = ''


thread_grant_access = threading.Thread(target=grant_access)
thread_cli = threading.Thread(target=looping_cli)
thread_background_command = threading.Thread(target=looping_background_command)


def give_access():
    global thread_grant_access
    if not thread_grant_access.is_alive():
        thread_grant_access = threading.Thread(target=grant_access)
        thread_grant_access.start()


if __name__ == '__main__':
    main()
