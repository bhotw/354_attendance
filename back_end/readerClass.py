import functions

class readerClass:
    def __init__(self):

    def destroy():
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

        id, name = read()
        present_time = get_time()
        meta_data = [present_time + get_action(action)]
        attendance_statistics[name] = meta_data


        with open('attendance_sheet.' + present_time + '.csv', 'w') as f:
            [f.write('{0}  {1}\n'.format(key, value))]
