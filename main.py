
# import back_end.readerClass as re

import time
# from tts import TTS

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from luma.core.interface.serial import spi, noop

serial = spi(port = 0, device = 1, gpio = noop())

reader = SimpleMFRC522()

def get_time():
    time.time()


    current_time = time.localtime(time.time)

    return current_time

class readerClass:
    # def __init__(self):
    #     self
    def destroy(self):
        GPIO.cleanup()

    def read(self):
        print("TAP to read Data!")
        id, text = reader.read()
        return id, text


    def write(self):
        data = input('Programing new Data /n Full Name:')
        print("TAP to write new Data!")
        reader.write(data)
        print("Data writing is complete.")

    def get_action(self, s):
        action = str()
        if (s == "in"):
            action = "Sign In"
        elif (s == "out"):
            action = "Sign Out"
        return action

    def attendance(self, action):
        attendance_statistics = {}

        id, name = readerClass.read()
        present_time = get_time()
        meta_data = [present_time + readerClass.get_action(action)]
        attendance_statistics[name] = meta_data


        with open('attendance_sheet.' + present_time + '.csv', 'w') as f:
            [f.write('{0}  {1}\n'.format(name, attendance_statistics))]



newReader = readerClass()

newReader.attendance("in")
