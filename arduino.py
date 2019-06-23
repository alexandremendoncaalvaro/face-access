from pyfirmata2 import Arduino
from config import ConfigArduino


class ArduinoBoard():
    def __init__(self):
        self.board = Arduino(ConfigArduino.USB_PATH) if ConfigArduino.USB_PATH != '' else Arduino(Arduino.AUTODETECT)
    def set_relay(self, enable):
        self.board.digital[8].write(enable) #Relay
        self.board.digital[9].write(enable) #Optional LED