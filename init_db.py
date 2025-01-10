# this has to run before the app starts to run this file will create 
# all the neccery databases
from attendance import app
from attendance import db
from back_end.models import *
from back_end.admin.models import *

with app.app_context():
    db.create_all()

