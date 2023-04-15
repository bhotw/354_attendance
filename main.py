
import back_end.readerClass as re
# from tts import TTS



# import time
#
# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522
# from luma.core.interface.serial import spi, noop
#
# serial = spi(port = 0, device = 1, gpio = noop())
#
# reader = SimpleMFRC522()
#
# def get_time():
#     time.time()
#
#     year = str(se.time.strftime('%Y', se.time.localtime(se.time.time())))
#     month = str(se.time.strftime('%m', time.localtime(time.time())))
#     day = str(time.strftime('d', time.localtime(time.time())))
#     hour = str(time.strftime('%H', time.localtime(time.time())))
#     minute = str(time.strftime('%M', time.localtime(time.time())))
#     second = str(time.strftime('%S', time.localtime(time.time())))
#
#     current_time = hour + '.' + minute + '.' + second + " : " + month + '.' + day + '.' + year
#
#     # current_time = time.localtime(time.time())
#
#     return current_time
#
# class readerClass:
#     # def __init__(self):
#     #     self
#     def destroy(self):
#         GPIO.cleanup()
#
#     def read(self):
#         print("TAP to read Data!")
#         id, text = reader.read()
#         return id, text
#
#
#     def write(self):
#         data = input('Programing new Data /n Full Name:')
#         print("TAP to write new Data!")
#         reader.write(data)
#         print("Data writing is complete.")
#
#     def get_action(self, s):
#         action = str()
#         if (s == "in"):
#             action = "Sign In"
#         elif (s == "out"):
#             action = "Sign Out"
#         return action
#
#     def attendance(self, action):
#         attendance_statistics = {}
#
#         id, name = readerClass.read(self)
#         present_time = get_time()
#         meta_data = [present_time , readerClass.get_action(self, action)]
#         attendance_statistics[name] = meta_data
#
#
#         with open('attendance_sheet.' + str(present_time) + '.csv', 'w') as f:
#             [f.write('{0}  {1}\n'.format(name, attendance_statistics))]
#


newReader = re.readerClass()

# def greetins(self):
#     id, name = newReader.read()
#     greeting = name + " Welcome!!"
#     tts.say(greeting)
#
#
# def bye(self):
#     id, name = newReader.read()
#     bye = name + " It was nice to see you today. Have a good one!!!"
#     tts.say(bye)

while True:
    try:
        action = input("Sign in or Sign out: ")
        if action == " Sign in":
            newReader.attendance("in")
            # greetins()
        elif action == "Sign out":
            newReader.attendance("out")
            # bye()
        else:
            print("Action not RECOGNIZED!!! Try again")
    except KeyboardInterrupt:
        newReader.destroy()
        break

