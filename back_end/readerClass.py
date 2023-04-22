

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# from dataMan import DataMan as DataMan
from back_end.dataMan import DataMan

reader = SimpleMFRC522()


class ReaderClass:
    # def __init__(self):
    #     self
    def destroy(self):
        GPIO.cleanup()

    def read(self):
        print("TAP to read Data!")
        reader_id, name = reader.read()
        return reader_id, name


    def write(self, data):

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

        current_time = hour + ':' + minute + ':' + second
        current_date = month + '-' + day + '-' + year

        return current_date, current_time

    def greetins(self):
        reader_id, reader_name = self.read()
        greeting = reader_name + " Welcome!!"
        print(greeting)

    def bye(self):
        reader_id, reader_name = self.read()
        bye = reader_name + " It was nice to see you today. Have a good one!!!"
        print(bye)

    def attendance(self, act):

        reader_id, reader_name = self.read()

        if DataMan.isMember(reader_id, reader_name):
            role = DataMan.getRole(reader_id, reader_name)
            present_date, present_time = self.get_time()
            action =  self.get_action(act)

            DataMan.addToSignInSheet(reader_id, reader_name, role, action, present_date, present_time)
        else:
            return "Id not Recognized. Try again"


    def showTable(self, howMany = "all"):

        if howMany == "one":
            DataMan.print(self)
        elif howMany == "all":
            DataMan.printAll(self)
        else:
            print("Try: one or all")

    def regidterNewMember(self):

        name = input("Name: ")
        role = input("Role: ")
        if role == "mentor":
            table_name = "mentors"
        elif role == "student":
            table_name = "students"

        current_date, current_time = self.get_time()
        self.write(name)

        reader_id, reader_name = self.read()
        DataMan.registration(table_name, reader_id, reader_name, role, current_date, current_time)



