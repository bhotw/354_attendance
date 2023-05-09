
# When we are setting up the app if you run this file it will create all the tables that are needed.
# or we name this something else and store it somewhere else so that we can have only one setup.py
# that will make sure that we get all the denpendency downloaded and installed. and then we have to
# fireup psql and create a database and run one more file to create all the tables and then are all set.
# I don't think creating the database and the user on the database can be automated so, we will have to see.

from back_end.dataBaseConfig import conn, cursor

cursor.execute("CREATE TABLE [IF NOT EXISTS] mentors ("
               "reader_id INT PRIMARY KEY NOT NULL, "
               "reader_name VARCHAR ( 70 ) NOT NULL,"
               "role VARCHAR ( 20 ) NOT NULL,"
               "Date date NOT NULL,"
               "Time time NOT NULL,"
               ""
               
               ")")
print("Mentos table creation successful.")

cursor.execute("CREATE TABLE students ("
               "reader_id INT PRIMARY KEY NOT NULL, "
               "reader_name VARCHAR ( 70 ) NOT NULL,"
               "role VARCHAR ( 20 ) NOT NULL,"
               ""

               ")")

