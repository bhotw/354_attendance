
import back_end.dataBaseConfig as data_base
# import dataBaseConfig as data_base

newDB = data_base.cursor

class DataMan:
    # def __init__(self):

    def createTable(self, table_name):
        newDB.execute("CREATE TABLE (%S) (ID integer, firstName text, lastName text, Action text, Role text", table_name)

    def addToTable(self, meta_data, table_name):
        # reader_id , first_name, last_name, action, role = meta_data
        # newDB.execute("INSERT INTO (%s) VALUES('reader_id', 'first_name','last_name', 'action', 'role' )", (reader_id , first_name, last_name, action, role) )
        #
        newDB.execute("INSERT INTO (Students) VALUES('meta_data')")


    def print(self):
        print(newDB.fetchone())

