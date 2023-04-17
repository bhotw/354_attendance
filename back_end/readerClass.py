

import time
import RPi.GPIO as GPIO
from mfrc522 import Simpl

from dataMan import DataMan

reader = SimpleMFRC522()


class ReaderClass:
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

        year = str(time.strftime('%Y', time.localtime(time.time())))
        month = str(time.strftime('%m', time.localtime(time.time())))
        day = str(time.strftime('%d', time.localtime(time.time())))
        hour = str(time.strftime('%H', time.localtime(time.time())))
        minute = str(time.strftime('%M', time.localtime(time.time())))
        second = str(time.strftime('%S', time.localtime(time.time())))

        current_time = hour + '.' + minute + '.' + second + " : " + month + '.' + day + '.' + year

        return current_time

    def greetins(self):
        id, name = self.read()
        greeting = name + " Welcome!!"
        print(greeting)

    def bye(self):
        id, name = self.read()
        bye = name + " It was nice to see you today. Have a good one!!!"
        print(bye)

    def attendance(self, action):
        attendance_statistics = {}

        id, name = self.read()
        present_time = self.get_time()
        meta_data = [present_time + " " + readerClass.get_action(action)]
        attendance_statistics[name] = meta_data

        table_name = "students"

        DataMan.addToTable(self, attendance_statistics, table_name)

        # with open('attendance_sheet.' + str(present_time) + '.csv', 'w') as f:
        #     [f.write('{0}\n'.format(attendance_statistics))]

    def showTable(self):
        self.DataMan.print()
