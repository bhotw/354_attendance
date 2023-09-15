# this has to run before the app starts to run this file will create 
# all the neccery databases

from attendance import db
from back_end.models import *

db.create_all()

