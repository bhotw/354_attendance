import time
# from tts import TTS

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from luma.core.interface.serial import spi, noop

serial = spi(port = 0, device = 1, gpio = noop())

reader = SimpleMFRC522()


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

    def get_time(self):
        # sys.time.time()

        year = str(time.strftime('%Y', time.localtime(time.time())))
        month = str(time.strftime('%m', time.localtime(time.time())))
        day = str(time.strftime('d', time.localtime(time.time())))
        hour = str(time.strftime('%H', time.localtime(time.time())))
        minute = str(time.strftime('%M', time.localtime(time.time())))
        second = str(time.strftime('%S', time.localtime(time.time())))

        current_time = hour + '.' + minute + '.' + second + " : " + month + '.' + day + '.' + year
        # current_time = se.time.localtime(se.time.time)

        return current_time


    def attendance(self, action):
        attendance_statistics = {}

        id, name = readerClass.read(self)
        present_time = readerClass.get_time(self)
        meta_data = [present_time + " " + readerClass.get_action(self,action)]
        attendance_statistics[name] = meta_data


        with open('attendance_sheet.' + str(present_time) + '.csv', 'w') as f:
            [f.write('{0}\n'.format(attendance_statistics))]
