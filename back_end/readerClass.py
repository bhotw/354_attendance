
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import threading

GPIO.setwarnings(False)


class ReaderClass:

    def __init__(self):
        self.reader = SimpleMFRC522()
        self.card_detected = None
        self.scanning = False

    def destroy(self):
        GPIO.cleanup()
        print("Reader cleaned up")

    def _scan_card(self, timeout):
        """Perform the actual scanning in a separate thread."""
        start_time = time.time()
        while self.scanning and (time.time() - start_time < timeout):
            try:
                status, TagType = self.reader.READER.MFRC522_Request(self.reader.READER.PICC_REQIDL)
                if status == self.reader.READER.MI_OK:
                    reader_id, _ = self.reader.read()
                    print(f"Card detected: {reader_id}")
                    self.card_detected = reader_id
                    self.scanning = False
                    return
            except Exception as e:
                print(f"RFID Reader Error: {e}")
                break
            time.sleep(0.5)

        print("Reader stopped after timeout.")
        self.scanning = False

    def read_only_id(self, timeout=10):
        """ Reads RFID but stops after timeout if no card is detected. """
        self.scanning = True
        self.card_detected = None

        scan_thread = threading.Thread(target=self._scan_card, args=(timeout,))
        scan_thread.start()

        scan_thread.join(timeout)

        self.destroy()
        return self.card_detected

    def write_name(self, data, timeout=10):
        """Writes data to the card if detected."""
        self.scanning = True
        self.card_detected = None

        scan_thread = threading.Thread(target=self._scan_card, args=(timeout,))
        scan_thread.start()

        scan_thread.join(timeout)

        if self.card_detected:
            reader_id, name = self.reader.write(data)
            self.destroy()
            return reader_id, name
        else:
            print("Timeout: No card detected to write data.")
            self.destroy()
            return None

    def read_id_name(self, timeout=10):
        """Reads the card ID and name."""
        self.scanning = True
        self.card_detected = None

        scan_thread = threading.Thread(target=self._scan_card, args=(timeout,))
        scan_thread.start()

        scan_thread.join(timeout)

        if self.card_detected:
            reader_id, name = self.reader.read()
            self.destroy()
            return reader_id, name
        else:
            print("Timeout: No card detected.")
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
