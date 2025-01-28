from attendance import app
from back_end.extensions import db
from back_end.models import *
from back_end.admin.models import *
from sqlalchemy import inspect

with app.app_context():
    db.create_all()  # This will create the tables

    # Get the list of all tables in the database
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    # Print the tables to confirm their creation
    print("Tables in the database:", tables)

    # Optionally, you can check and print each table's columns
    for table in tables:
        columns = inspector.get_columns(table)
        print(f"Columns in {table}: {[column['name'] for column in columns]}")
