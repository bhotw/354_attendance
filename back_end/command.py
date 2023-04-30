
from back_end.readerClass import ReaderClass
from back_end.dataMan import DataMan

class Command:

    def sign_in(self,reader_id, reader_name):
        action = "Sign In"
        reader_id, reader_name = ReaderClass.read()

        if DataMan.isMember(reader_id, reader_name):
            role = DataMan.getRole(reader_id, reader_name)
            present_date, present_time = ReaderClass.get_time()

            DataMan.addToSignInSheet(reader_id, reader_name, role, action, present_date, present_time)
            return "Sing In Successful. Hi there how are you dong today."
        else:
            return "Id not Recognized. Try again"
        
        
    def sign_out(self,reader_id, reader_name ):
        action = "Sign Out"

        if DataMan.isMember(reader_id, reader_name):
            if DataMan.isSignedIn():

                role = DataMan.getRole(reader_id, reader_name)
                present_date, present_time = ReaderClass.get_time()
                DataMan.addToSignInSheet(reader_id, reader_name, role, action, present_date, present_time)

                hours = DataMan.getDayHours(reader_id)
                DataMan.addToTotalHours(reader_id, hours)
                return "Sign out Successful, Byeeeeeee"
            
            else:

                role = DataMan.getRole(reader_id, reader_name)
                present_date, present_time = ReaderClass.get_time()
                DataMan.addToSignInSheet(reader_id, reader_name, role, action, present_date, present_time)
                return "You never Signed In. But your Sign Out was logged. Byeeeeee"

        else:
            return "Id not Recognized. Try again"

    def get_status(self, reader_id, reader_name):

        present_date, present_time = ReaderClass.get_time(ReaderClass)
        sign_in_time = DataMan.getSignInTime(reader_id, reader_name)
        if DataMan.isSignedIn(reader_id, reader_name, present_date):
            message = "Hi" + reader_name + "You have Signed in at " + sign_in_time
        else:
            message = "You did not Sing In today yet. Try Sign in."

        return message




    def regidterNewMember(self, name, role, ):

        name = input("Name: ")
        role = input("Role: ")
        if role == "mentor":
            table_name = "mentors"
        elif role == "student":
            table_name = "students"

        current_date, current_time = ReaderClass.get_time()
        ReaderClass.write(name)

        reader_id, reader_name = ReaderClass.read()
        DataMan.registration(table_name, reader_id, reader_name, role, current_date, current_time)



