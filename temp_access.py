import os
import base64
import cv2
import pyotp
import pyqrcode
import png
from pyzbar import pyzbar
from cryptography.fernet import Fernet
from config import ConfigTempAccess


class OneTimePassword():
    def __init__(self):
        self.totp = pyotp.TOTP(ConfigTempAccess.BASE_32_KEY)

    def get_new_base32_key(self):
        return pyotp.random_base32()

    def verify(self, verification_key):
        result = self.totp.verify(verification_key)
        return result


class QrCode():
    def __init__(self):
        self.crypto = Crypto()
        self.last_barcode_data = ''

    def get_qr_codes(self, frame):
        barcodes = pyzbar.decode(frame)
        barcodes_data = []
        if len(barcodes) > 0:
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                barcodes_data.append(barcode_data)
                if self.last_barcode_data == barcode_data:
                    try:
                        decrypted_message = self.crypto.decrypt(
                            barcode_data).decode('utf-8')
                        self.paint_frame(frame, decrypted_message,
                                         barcode.rect, color=ConfigTempAccess.QrCodeColor.encrypted)
                    except:
                        self.paint_frame(frame, barcode_data, barcode.rect)

                else:
                    self.last_barcode_data = barcode_data
                    self.paint_frame(frame, barcode_data, barcode.rect)

        return barcodes_data, frame

    def paint_frame(self, frame, barcode_data, barcode_rect, color=ConfigTempAccess.QrCodeColor.default):
        (x, y, w, h) = barcode_rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, barcode_data, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def generate(self, message):
        encrypted = self.crypto.encrypt(message)
        qr = pyqrcode.create(encrypted)
        qr.png(f'./qrcodes/{message}.png', 10)
        qr.show()


class Crypto():
    def generate_key(self):
        key = Fernet.generate_key()
        file = open('crypto.key', 'wb')
        file.write(key)
        file.close()

    def get_key(self):
        exists = os.path.isfile('crypto.key')
        if not exists:
            self.generate_key()
        file = open('crypto.key', 'rb')
        key = file.read()
        file.close()

        return key

    def encrypt(self, message):
        key = self.get_key()
        f = Fernet(key)

        cipher = f.encrypt(message.encode('utf-8'))
        encrypted = base64.b64encode(cipher)
        result = encrypted
        return result

    def decrypt(self, encrypted):
        key = self.get_key()
        f = Fernet(key)

        cipher = base64.b64decode(bytes(encrypted, 'utf-8'))
        message = f.decrypt(cipher)
        return message
