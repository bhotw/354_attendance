
from back_end.readerClass import ReaderClass
from back_end.dataMan import DataMan

class Command:

    def sign_in(self):
        action = "Sign In"
        reader_id, reader_name = ReaderClass.read()

        if DataMan.isMember(reader_id, reader_name):
            role = DataMan.getRole(reader_id, reader_name)
            present_date, present_time = ReaderClass.get_time()

            DataMan.addToSignInSheet(reader_id, reader_name, role, action, present_date, present_time)
        else:
            return "Id not Recognized. Try again"
        
        
    def sign_out(self, ):
        action = "Sign Out"
        reader_id, reader_name = ReaderClass.read()

        if DataMan.isMember(reader_id, reader_name):
            if DataMan.isSignedIn():

                role = DataMan.getRole(reader_id, reader_name)
                sign_in_time = DataMan.getSignInTime(reader_id, reader_name)
                present_date, present_time = ReaderClass.get_time()
                DataMan.addToSignInSheet(reader_id, reader_name, role, action, present_date, present_time)
                DataMan.addToTotalHours(reader_id, hours)
                return "Sign out Success full, Byeeeeeee"
            
            else:

                role = DataMan.getRole(reader_id, reader_name)
                present_date, present_time = ReaderClass.get_time()
                DataMan.addToSignInSheet(reader_id, reader_name, role, action, present_date, present_time)
                return "You never Signed In. But your Sign Out was logged. byeeeeee"

        else:
            return "Id not Recognized. Try again"




    def regidterNewMember(self, name, role, ):

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



