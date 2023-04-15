import functions
function = functions.get_time()

class readerClass:
    # def __init__(self):
    #     self
    def destroy(self):
        function.GPIO.cleanup()

    def read(self):
        print("TAP to read Data!")
        id, text = function.reader.read()
        return id, text


    def write(self):
        data = input('Programing new Data /n Full Name:')
        print("TAP to write new Data!")
        function.reader.write(data)
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

        id, name = readerClass.read(self)
        present_time = readerClass.get_time(self)
        meta_data = [present_time + readerClass.get_action(self,action)]
        attendance_statistics[name] = meta_data


        with open('attendance_sheet.' + str(present_time) + '.csv', 'w') as f:
            [f.write('{0}  {1}\n'.format(name, attendance_statistics))]
