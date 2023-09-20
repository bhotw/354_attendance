

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from back_end.dataMan import cursor, conn                        

# from dataMan import DataMan as DataMan
from back_end.dataMan import DataMan

reader = SimpleMFRC522()
GPIO.setwarnings(False)




class ReaderClass:
    # def __init__(self):
    #     self
    def destroy(self):
        GPIO.cleanup()
        print("reader clean")

    def read(self):
        print("TAP to read Data!")
        reader_id, name = reader.read()

        print(reader_id, ": ", name)
        return reader_id, name


    def write(self, data):

        print("TAP to write new Data!")
        reader.write(data)
        print("Data writing is complete.")



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


    def manual_registration(self):
        name = input("Name: ")
        role = input("Role: ")

        if role == "student":
            self.write(name)
            print("TAP again to complete registration")
            present_date, present_time = self.get_time()
            reader_id, reader_name = self.read()
            cursor.execute("INSERT INTO students (id, name, role, date, time) VALUES(%s, %s, %s, %s, %s)", (reader_id, reader_name, role, present_date, present_time,))
            conn.commit()
        elif role == "mentor":
            self.write(name)
            print("TAP again to complete registration")
            present_date, present_time = self.get_time()
            reader_id, reader_name = self.read()
            cursor.execute("INSERT INTO mentors (id, name, role, date, time) VALUES(%s, %s, %s, %s, %s)", (reader_id, reader_name, role, present_date, present_time,))
            conn.commit()

    def greetins(self):
        reader_id, reader_name = self.read()
        greeting = reader_name + " Welcome!!"
        print(greeting)

    def bye(self):
        reader_id, reader_name = self.read()
        bye = reader_name + " It was nice to see you today. Have a good one!!!"
        print(bye)

 
