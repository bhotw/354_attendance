
from back_end.readerClass import ReaderClass
from back_end.dataMan import DataMan

class Command:

    def sign_in(self,reader_id, reader_name):
        action = "Sign In"

        if DataMan.isMember("self",reader_id, reader_name):
            if not DataMan.isSignedIn("self"):
                role = DataMan.getRole("self",reader_id, reader_name)
                present_date, present_time = ReaderClass.get_time("self")

                DataMan.addToSignInSheet("self",reader_id, reader_name, role, action, present_date, present_time)
                message = [reader_name, action, present_time, present_date]
            else:
                message = self.get_status(reader_id, reader_name)
        else:
            message = "Id not Recognized. Try again"

        return message
        
        
    def sign_out(self,reader_id, reader_name ):
        action = "Sign Out"

        if DataMan.isMember("Self",reader_id, reader_name):
            if DataMan.isSignedIn("self"):

                role = DataMan.getRole("self",reader_id, reader_name)
                present_date, present_time = ReaderClass.get_time("self")
                DataMan.addToSignInSheet("self",reader_id, reader_name, role, action, present_date, present_time)

                hours = DataMan.getDayHours("self",reader_id)
                DataMan.addToTotalHours("self",reader_id, hours)

                message = [reader_name, action, present_time, present_date]
            
            else:

                role = DataMan.getRole("self",reader_id, reader_name)
                present_date, present_time = ReaderClass.get_time("self")
                DataMan.addToSignInSheet(reader_id, reader_name, role, action, present_date, present_time)

                message = [reader_name, action, present_time, present_date, "You did not Signed In Today. But your Sign Out was logged." ]

        else:
            message = "Id not Recognized. Try again"

        return message

    def get_status(self, reader_id, reader_name):

        present_date, present_time = ReaderClass.get_time("self")
        if DataMan.isSignedIn("self",reader_id, reader_name, present_date):
            sign_in_time = DataMan.getSignInTime("self",reader_id, reader_name)
            message = ["Active", reader_name, sign_in_time]
        else:
            message = ["Not Active",reader_name, "You did not Sing In today yet. You have to SIGN IN."]
            print(message)

        return message

    def get_info(self, reader_id, reader_name):

        role = DataMan.getRole("self", reader_id, reader_name)  # this don't work yet coz the table don't exist.
        #role = "Smart"
        message = [reader_id, reader_name, role]

        return message




    def regidterNewMember(self, name, role, ):

        # name = input("Name: ")
        # role = input("Role: ")
        if role == "mentor":
            table_name = "mentors"
        elif role == "student":
            table_name = "students"

        current_date, current_time = ReaderClass.get_time("self")
        ReaderClass.write(name)

        reader_id, reader_name = ReaderClass.read()
        DataMan.registration(table_name, reader_id, reader_name, role, current_date, current_time)



