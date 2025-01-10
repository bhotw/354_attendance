from _curses import flash
from back_end.admin.routes import admin_bp
from flask import Flask, render_template, request, Response, stream_with_context, redirect, url_for
from back_end.database import db
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import time

# Import your custom modules and classes
from back_end.readerClass import ReaderClass
from back_end.controllers.registration import Registration
from back_end.controllers.sign_in import sign_in
from back_end.controllers.is_member import is_member
from back_end.controllers.mentor_authorization import mentor_authorization
from back_end.controllers.get_status import get_status
from back_end.controllers.get_register import get_register
from back_end.models import User, Attendance, WorkshopHours
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY

load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # Set the configuration
app.config['SECRET_KEY'] = SECRET_KEY
db.init_app(app)

app.register_blueprint(admin_bp)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'


csrf = CSRFProtect(app)
reader = ReaderClass()


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
            is_a_member = is_member(reader_id, reader_name)
            if is_a_member:
                # Add the attendance record to the database
                result = sign_in(id=reader_id, date=present_date, sign_in_time=present_time)
                db.session.add(result)
                db.commit()
                # message = [reader_name, "Sign in", present_time, present_date]
                yield render_template('present_message.html', action="sign_in", message="Sign In Successful!!!")
            else:
                message = "You are not a member. Please contact a mentor for assistance."
                yield render_template('present_message.html', action="sign_in", message=message)

            reader.destroy()
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

            mentor_auth = mentor_authorization(reader_id)
            print(mentor_auth)
            if mentor_auth:
                yield render_template('present_message.html', action="sign_out", message="TAP To Sign Out")
                reader_id, reader_name = reader.read()
                present_date, present_time = reader.get_time()
                is_a_member = is_member(reader_id, reader_name)

                if is_a_member:
                    # Call the sign_out function to handle the sign-out process
                    result = sign_out(id=reader_id, date=present_date, sign_out_time=present_time)

                    yield render_template('present_message.html', action="sign_out", message=result)
                else:
                    # Handle the case when the person is not a member
                    message = "You are not a member. Please contact a mentor for assistance."
                    yield render_template('present_message.html', action="sign_out", message=message)

                time.sleep(30)
                yield render_template('home.html')
                reader.destroy()
            else:
                yield render_template('sign_out.html')

        return Response(stream_with_context(present_sign_out()))


@app.route("/get_info", methods=['GET', 'POST'])
def get_info():
    if request.method == 'GET':
        def present_info():
            yield render_template('get_info.html')
            reader_id, reader_name = reader.read()

            # Check if the user is a member
            is_a_member = is_member(reader_id, reader_name)

            if is_a_member:
                # Call the get_info function to retrieve user information
                result = get_info(id=reader_id, name=reader_name)

                yield render_template('present_message.html', action="info", message=result)
            else:
                # Handle the case when the person is not a member
                message = "You are not a member. Please contact a mentor for assistance."
                yield render_template('present_message.html', action="info", message=message)

            time.sleep(30)
            yield render_template('home.html')
            reader.destroy()

        return Response(stream_with_context(present_info()))

@app.route("/register", methods=[ 'POST'])
def register():
    form = Registration()

    if request.method == 'POST' and form.validate_on_submit():
        # Read card ID
        yield render_template('present_message.html', message="Tap a NEW card.")
        card_id = reader.read()

        # Form data retrieval
        name = form.name.data
        role = form.role.data
        email = form.email.data
        phone = form.phone.data
        emergency_contact = form.emergency_contact.data
        emergency_phone = form.emergency_phone.data
        parent_email = form.parent_email.data

        # Call the function to register the member
        result = get_register(card_id, name, role, email, phone, emergency_contact, emergency_phone, parent_email)

        if result == "User registered successfully":
            flash("New member has been registered successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Registration failed. Please try again.", "error")

    # Render the form template for GET or validation failure
    return render_template('register.html', title='Registration', form=form)


@app.route("/status")
def status():
    if request.method == 'GET':
        def present_status():
            yield render_template('status.html')
            reader_id, reader_name = reader.read()
            present_date, present_time = reader.get_time()

            # Check if the user is a member
            is_a_member = is_member(reader_id, reader_name)

            if is_member:
                # Call the get_status function to retrieve the user's status
                result = get_status(reader_id)

                yield render_template('present_message.html', action="status", message=result)
            else:
                # Handle the case when the person is not a member
                message = "You are not a member. Please contact a mentor for assistance."
                yield render_template('present_message.html', action="status", message=message)

            time.sleep(30)
            yield render_template('home.html')
            reader.destroy()

        return Response(stream_with_context(present_status()))


# @app.route("/admin")
# def admin():
#     return render_template('admin.html')


@app.route("/clear", methods=['GET'])
def clear():
    if request.method == 'GET':
        reader.destroy()
        return redirect(url_for('home'))
