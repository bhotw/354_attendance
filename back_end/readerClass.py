
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)


class ReaderClass:
    def __init__(self):
        self.reader = SimpleMFRC522()
    def destroy(self):
        GPIO.cleanup()
        print("reader clean")

    def read_only_id(self):
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            reader_id, _ = self.reader.read()
            return reader_id
            time.sleep(10)
        print("Tap a Card!")
        return None
	
    def read_id_name(self):
        print("TAP to read Data!")
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            reader_id, name = self.reader.read()
            return reader_id, name
            time.sleep(10)
        return None


    def write_name(self, data):
        print("Tap a Card to write!")
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            reader_id, name = self.reader.write(data)
            return reader_id, name
            time.sleep(10)
        return None


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
