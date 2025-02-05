

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)
reader = SimpleMFRC522()





class ReaderClass:
    def destroy(self):
        GPIO.cleanup()
        print("reader clean")

    def read_id(self):
        print("Tap a Card!")
        reader_id = reader.read_id()
        return reader_id
	
    def read(self):
        print("TAP to read Data!")
        reader_id, name = reader.read()

        return reader_id, name

    def write(self, data):
        print("Tap a Card to write!")
        reader.write(data)
        return ["success", data]


    def get_time(self):

        year = str(time.strftime('%Y', time.localtime(time.time())))
        month = str(time.strftime('%m', time.localtime(time.time())))
        day = str(time.strftime('%d', time.localtime(time.time())))
        hour = str(time.strftime('%H', time.localtime(time.time())))
        minute = str(time.strftime('%M', time.localtime(time.time())))
        second = str(time.strftime('%S', time.localtime(time.time())))

        current_time = hour + ':' + minute + ':' + second
        current_date = month + '-' + day + '-' + year

        return current_date, current_time


 
