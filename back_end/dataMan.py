
from back_end.dataBaseConfig import cursor, conn

class DataMan:
    # def __init__(self):

    def getRole(self, reader_id, reader_name):
        stored_name = cursor.execute("SELECT name FROM students")
        stored_id = cursor.execute("SELECT reader_id FROM students")

        if stored_name == reader_name and stored_id == reader_id:
            return "student"
        else:
            stored_name = cursor.execute("SELECT name FROM mentors")
            stored_id = cursor.execute("SELECT reader_id FROM mentors")

            if stored_name == reader_name and stored_id == reader_id:
                return "mentor"

        # this needs to be tested and see how the data comes out from the tables and stuff.
        # the function is pretty much done but not tested.

    def getSignInTime(self, reader_id, reader_name, present_date):
         
         sing_in_time = cursor.execute("SELECT time FROM sign_in_sheet WHERE id = %s AND name = %s AND date = %s", (reader_id, reader_name, present_date))

         return sing_in_time


    def isMember(self, reader_id, reader_name):

        if self.getRole(reader_id, reader_name) == "mentor" or "student":
            return True
        else:
            return False
        

    def isSignedIn(self, reader_id, reader_name, present_date):

        stored_name = cursor.execute("SELECT name FROM sign_in_sheet WHERE id = %s AND date = %s", (reader_id, present_date))
        if reader_name == stored_name:
            return True
        else:
            return False

        # this function returns true when the member is signed in for the day



    def getDayHours(self, reader_id, reader_name, present_date, present_time):

        hours = 0

        if self.isSignedIn(reader_id, reader_name, present_date):
            logged_time = self.getSignInTime(reader_id, reader_name, present_date)
            hours = present_time - logged_time

        return hours

        # this will return the amount of hours they spent that day.



    def registration(self, table_name, reader_id, reader_name, role, present_date, present_time):
        cursor.execute("INSERT INTO %s (id, name, role, date, time) VALUES(%s, %s, %s, %s, %s)", (table_name, reader_id, reader_name, role, present_date, present_time,) )
        conn.commit()

        message = ("New member %s was added %s", reader_name, table_name)
        print(message)
        print(message)

    def addToSignInSheet(self, reader_id, reader_name, role, action, present_date, present_time):

        cursor.execute("INSERT INTO sign_in_sheet (id, name, role, action, date, time) VALUES(%s, %s, %s, %s, %s)", (reader_id, reader_name, role, action, present_date, present_time,) )
        conn.commit()

        message = "%s %s added to Sign in Sheet", reader_name, action
        print(message)
        return message

    def addToTotalHours(self, reader_id, hours):

        old_hours = cursor.execute("SELECT hours FROM total_hours WHERE id=%s", (reader_id,))
        new_hours = old_hours + hours

        cursor.execute("Update total_hours set hours = %s where id = %s", (new_hours,reader_id))
        conn.commit()

        message = "Total Hours Updated."
        print(message)
        return message

    def addToHours(self, reader_id, reader_name, hours, present_date, present_time):

        cursor.execute("INSERT INTO hours(id, name, hour, date, time) VALUES(%s, %s, %s, %s)", (reader_id, reader_name, hours, present_date, present_time,))
        conn.commit()
        self.addToTotalHours(reader_id, hours)

        message = "Added to hours table."
        print(message)
        return message


    def print(self):
        cursor.execute("SELECT * FROM students")
        print(cursor.fetchone())

    def printAll(self):
        cursor.execute("SELECT * FROM students")
        print(cursor.fetchall())

