
from back_end.dataBaseConfig import cursor, conn
# import dataBaseConfig as data_base

# newDB = data_base.cursor()

class DataMan:
    # def __init__(self):

    def registration(self, table_name, reader_id, name, role, present_date, present_time):
        cursor.execute("INSERT INTO %s (id, name, role, date, time) VALUES(%s, %s, %s, %s, %s)", (table_name, reader_id, name, role, present_date, present_time,) )
        conn.commit()

        print("New member %s was added %s", name, table_name)

    def addToSignInSheet(self, reader_id, name, role, action, present_date, present_time):
        cursor.execute("INSERT INTO sign_in_sheet (id, name, role, action, date, time) VALUES(%s, %s, %s, %s, %s)", (reader_id, name, role, action, present_date, present_time,) )

        # cursor.execute("INSERT INTO Students(name, school) VALUES(%s, %s)", (name, action,))
        conn.commit()
        print("%s %s added to Sign in Sheet", name, action)


    def print(self):
        cursor.execute("SELECT * FROM students")
        print(cursor.fetchone())

    def printAll(self):
        cursor.execute("SELECT * FROM students")
        print(cursor.fetchall())

