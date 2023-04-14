import back_end.functions as fs

class readerClass:
    # def __init__(self):
    #     self
    def destroy(self):
        fs.GPIO.cleanup()

    def read(self):
        print("TAP to read Data!")
        id, text = fs.reader.read()
        return id, text


    def write(self):
        data = input('Programing new Data /n Full Name:')
        print("TAP to write new Data!")
        fs.reader.write(data)
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

        id, name = fs.read()
        present_time = fs.get_time()
        meta_data = [present_time + fs.get_action(action)]
        attendance_statistics[name] = meta_data


        with open('attendance_sheet.' + present_time + '.csv', 'w') as f:
            [f.write('{0}  {1}\n'.format(key, value))]
