from pyzbar import pyzbar
import cv2
import pyotp

BASE_32_KEY = 'XCOBLUBMMAJND2GY'

class OneTimePassword():
    def __init__(self):
        self.totp = pyotp.TOTP(BASE_32_KEY)

    def get_new_base32_key(self):
        return pyotp.random_base32()

    def verify(self, verification_key):
        result = self.totp.verify(verification_key)
        return result


class QrCode():
    def get_qr_codes(self, frame):
        barcodes = pyzbar.decode(frame)
        barcodes_data = []

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            barcodes_data.append(barcode_data)
            self.paint_frame(frame, barcode_data, barcode.rect)

        return barcodes_data, frame

    def paint_frame(self, frame, barcode_data, barcode_rect):
        (x, y, w, h) = barcode_rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        text = "{}".format(barcode_data.replace('temp:', ''))
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
