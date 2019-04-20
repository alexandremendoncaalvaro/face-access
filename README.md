# Face Access

Basic example of access control with face recognition

Using: 
  * Python 3
  * OpenCV
  * [dlib](http://dlib.net/)
  * Face Recognition ([ageitgey](https://github.com/ageitgey/face_recognition))

Complete version:
  * Arduino ([pyfirmata](https://pypi.org/project/pyFirmata/))
  * Google Text 2 Speech ([gTTS](https://pypi.org/project/gTTS/))
  * QR-Code ([pyZbar](https://pypi.org/project/pyzbar/))

# Installation

## Python 3 + OpenCV
[Complete Tutorial from pyimagesearch](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/)

## DLib + Face Recognition (ageitgey)
### Requirements
  * Python 3.3+
  * macOS or Linux (Windows not officially supported, but might work)
  
#### Installing on Mac or Linux
First, make sure you have dlib already installed with Python bindings:
  * [How to install dlib from source on macOS or Ubuntu](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)

Then, install this module from pypi using `pip3`:

```bash
pip3 install face_recognition
```
#### Installing on Windows

While Windows isn't officially supported, helpful users have posted instructions on how to install this library:
  * [@masoudr's Windows 10 installation guide (dlib + face_recognition)](https://github.com/ageitgey/face_recognition/issues/175#issue-257710508)
  
## Arduino control with pyFirmata (optional)
You will need an Arduino Board like Uno, Mega, Micro, Nano with a relay module to control the access.
Install Arduino IDE and use the Example Firmata > StandardFirmata on the board.
The board need to stay connected by USB.
All the GPIO controll will be done by the python code.

Python 3 lib:
```bash
pip3 install pyFirmata
```

## Google Text 2 Speech
Python 3 lib:
```bash
pip3 install gTTS
```

## QR-Code
macOS users can simply install using Homebrew
```bash
brew install zbar
```
Ubuntu users can install using
```bash
sudo apt-get install libzbar-dev libzbar0
```
Python 3 lib:
```bash
pip3 install pyzbar
```

