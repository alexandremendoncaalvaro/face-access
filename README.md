# Face Access

Basic example of access control with face recognition
  * MIT License
  * LGPDP Brasil Safe (Lei Geral de Proteção de Dados Pessoais)

### Basic Version
- [x] Basic command line interface
- [x] Face recogniton from Webcam
- [x] Just need the photo for register. Save only a id on the database (file database).

### More Complete Version (already tested, just need to port to this code)
- [ ] Text to Speech for welcome audio message
- [ ] Arduino commands to open the door
- [ ] Qr-Code to easy registration and temporary access
- [ ] Audio code (CHIRP) to easy registration and temporary access

## After installation
To start, with terminal go to folder path and execute:
```bash
python3 main.py
```

## CLI commands:
If everything is right, a new window with the webcam streaming and face recognition will start.
In the terminal you should see somethong like: 

**CMD:**

### Where you can do some actions like:
*Don't use spaces between parameters, only between firstname, midlename, lastname..

Add a new face id from a image file in the folder images:
```bash
add,Joseph Smith,images/joseph.jpg
```

Add a new face id from the current webcam capture:
```bash
add,Joseph Smith
```

List the current face ids:
```bash
print
```

Remove a face id:
```bash
del,Joseph Smith
```

Exit:
```bash
q
```
or
```bash
quit
```

# Technologies and Libraries
  * Python 3
  * OpenCV
  * [dlib](http://dlib.net/)
  * Face Recognition ([ageitgey](https://github.com/ageitgey/face_recognition))

For complete version (already tested but not implemented yet):
  * Arduino ([pyfirmata](https://pypi.org/project/pyFirmata/))
  * Google Text 2 Speech ([gTTS](https://pypi.org/project/gTTS/))
  * QR-Code ([pyZbar](https://pypi.org/project/pyzbar/))
  * Audio-Code ([Chirp](https://developers.chirp.io/docs))
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
  
## Arduino control with pyFirmata (complete version)
You will need an Arduino Board like Uno, Mega, Micro, Nano with a relay module to control the access.
Install Arduino IDE and use the Example Firmata > StandardFirmata on the board.
The board need to stay connected by USB.
All the GPIO controll will be done by the python code.

Python 3 lib:
```bash
pip3 install pyFirmata
```

## Google Text 2 Speech (complete version)
Python 3 lib:
```bash
pip3 install gTTS
```

## QR-Code (complete version)
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

## Audio Code - CHIRP (complete version)
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
