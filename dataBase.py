import psycopg2

conn = psycopg2.connect(database="test",
                        host="127.0.0.1",
                        user="pitest",
                        password="pi_test",
                        port="5432")

cursor = conn.cursor()

cursor.execute("SELECT * FROM people")

print(cursor.fetchone())