
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import threading

GPIO.setwarnings(False)


class ReaderClass:
    # def __init__(self):
    #     self.reader = SimpleMFRC522()
    # def destroy(self):
    #     GPIO.cleanup()
    #     print("reader clean")

    # def read_only_id(self):
    #     timeout = 10
    #     start_time = time.time()
    #     while time.time() - start_time < timeout:
    #         reader_id, _ = self.reader.read()
    #         return reader_id
    #         time.sleep(0.5)
    #     print("Tap a Card!")
    #     self.destroy()
    #     return None

    def __init__(self):
        self.reader = SimpleMFRC522()
        self.card_detected = None  # Store detected card ID
        self.scanning = False  # Flag to control scanning

    def destroy(self):
        GPIO.cleanup()
        print("Reader cleaned up")

    def read_only_id(self, timeout=10):
        """ Reads RFID but stops after timeout. """
        start_time = time.time()
        self.scanning = True
        self.card_detected = None  # Reset

        def scan_card():
            nonlocal start_time
            while self.scanning and (time.time() - start_time < timeout):
                try:
                    status, TagType = self.reader.READER.MFRC522_Request(self.reader.READER.PICC_REQIDL)
                    if status == self.reader.READER.MI_OK:
                        reader_id, _ = self.reader.read()
                        print(f"Card detected: {reader_id}")
                        self.card_detected = reader_id
                        self.scanning = False  # Stop scanning
                        return
                except Exception as e:
                    print(f"RFID Reader Error: {e}")
                    break
                time.sleep(0.5)  # Prevent high CPU usage

            print("Reader stopped after timeout.")
            self.scanning = False  # Stop scanning

        # Run scan in a separate thread
        scan_thread = threading.Thread(target=scan_card)
        scan_thread.start()

        # Wait for the scan to finish (max `timeout` seconds)
        scan_thread.join(timeout)

        # Ensure cleanup
        self.destroy()
        return self.card_detected  # Return the detected card or None

    def read_id_name(self):
        print("TAP to read Data!")
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            reader_id, name = self.reader.read()
            return reader_id, name
            time.sleep(0.5)

        self.destroy()
        return None


    def write_name(self, data):
        print("Tap a Card to write!")
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            reader_id, name = self.reader.write(data)
            return reader_id, name
            time.sleep(0.5)

        self.destroy()
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
