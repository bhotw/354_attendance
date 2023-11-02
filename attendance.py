
from flask import Flask, render_template, request, Response, stream_with_context, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import time

# Import your custom modules and classes
from back_end.readerClass import ReaderClass
from back_end.controllers.registration import Registration
from back_end.controllers.sign_in import sign_in
from back_end.models import User
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # Set the configuration
app.config['SECRET_KEY'] = SECRET_KEY

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
reader = ReaderClass()
command = Command()


@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/")
def hello():
    return redirect('/home')


@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        def present_sign_in():
            yield render_template('sign_in.html')
            reader_id, reader_name = reader.read()
            present_date, present_time = reader.get_time()

            # Add the attendance record to the database
            result = sign_in(id=reader_id, date=present_date, sign_in_time=present_time)

            # message = [reader_name, "Sign in", present_time, present_date]
            yield render_template('present_message.html', action="sign_in", message=result)
            time.sleep(30)
            yield render_template('home.html')
            reader.destroy()

        return Response(stream_with_context(present_sign_in()))

@app.route("/sign_out", methods=['GET', 'POST'])
def sign_out():
    if request.method == 'GET':
        def present_sign_out():
            yield render_template('sign_out.html')
            reader_id, reader_name = reader.read()

            present_date, present_time = reader.get_time()
            message = [reader_name, "Sign in", present_time, present_date]
            # message = Command.sign_out("self",reader_id,reader_name)
            yield render_template('present_message.html', action="sign_out", message=message)
            time.sleep(30)
            yield render_template('home.html')
            ReaderClass.destroy("self")

        return Response(stream_with_context(present_sign_out()))





@app.route("/get_info", methods=['GET', 'POST'])
def get_info():
    if request.method == 'GET':
        def present_info():
            yield render_template('get_info.html')
            reader_id, reader_name = reader.read()
            message = command.get_info(reader_id, reader_name)
            yield render_template('present_message.html', action="info", message=message)
            time.sleep(30)
            yield render_template('home.html')
            reader.destroy()

        return Response(stream_with_context(present_info()))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = Registration()
    card_id = reader.read()
    if form.validate_on_submit():
        user = User(id=card_id, name=form.name, role=form.role, email=form.email, phone=form.phone,
                    emergency_contact=form.emergency_contact, emergency_phone=form.emergency_phone,
                    parent_email=form.parent_email)

        db.session.add(user)
        db.session.commit()

        flash('New Member has been added to the team!!!')
        return redirect(url_for('home'))
    return render_template('register.html', title='Registation', form=form)


#  this is the old code we shall see if the new code works. Only then we
#   we can get rid of the old code. I know they are all on github and on
#   other branch but I still want to keep them here for the time bring.
# if request.method == 'POST':
#     name = request.form["fullname"]
#     role = request.form["role"]
#     # def present_register():
#     #     yield render_template('register.html')
#     #     name = request.form("fullname")
#     #     role = request.form("role")
#     #     message = name + " " + role
#     #     print(message)
#     #     yield render_template('present_message.html', message=message)

#     # return Response(stream_with_context(present_register()))
#     print (name, " ", role)

# return render_template('register.html')

@attendance_bp.route("/status")
def status():
    if request.method == 'GET':
        def present_status():
            yield render_template('status.html')
            reader_id, reader_name = reader.read()
            message = command.get_status(reader_id, reader_name)
            yield render_template('present_message.html', action="status", message=message)
            time.sleep(30)
            yield render_template('home.html')
            reader.destroy()

        return Response(stream_with_context(present_status()))
    return render_template('status.html')


@attendance_bp.route("/admin")
def admin():
    return render_template('admin.html')


@attendance_bp.route("/clear", methods=['GET'])
def clear():
    if request.method == 'GET':
        reader.destroy()
        return redirect(url_for('my_blueprint.home'))






