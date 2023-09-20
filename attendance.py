
import os
from flask_sqlalchem import SQLAlchemy
from flask import Flask, render_template, request
from flask import Response, stream_with_context, redirect, url_for
from back_end.readerClass import ReaderClass
from back_end.command import Command
import time
from config import SQLALCHEMY_DATABASE_URL, SECRE_KEY

from back_end.controllers.registration import Registration
from back_end.models import User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = SQLALCHEMY_DATABASE_URL
app.config['SECRE_KEY'] = SECRE_KEY

db = SQLAlchemy(app)





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
            reader_id, reader_name = ReaderClass.read("self")
            present_date, present_time = ReaderClass.get_time("self")
            message = [reader_name, "Sign in", present_time, present_date]
            # message = Command.sign_in("self",reader_id,reader_name)
            yield render_template('present_message.html', action="sign_in", message=message)
            time.sleep(30)
            yield render_template('home.html')
            ReaderClass.destroy("self")
        return Response(stream_with_context(present_sign_in()))


@app.route("/sign_out", methods=['GET', 'POST'])
def sign_out():

    if request.method == 'GET':
        def present_sign_out():
            yield render_template('sign_out.html')
            reader_id, reader_name = ReaderClass.read("self")

            present_date, present_time = ReaderClass.get_time("self")
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
            reader_id, reader_name = ReaderClass.read("self")
            message = Command.get_info("self",reader_id,reader_name)
            yield render_template('present_message.html', action="info", message=message)
            time.sleep(30)
            yield render_template('home.html')
            ReaderClass.destroy("self")
        return Response(stream_with_context(present_info()))



@app.route("/register", methods=['GET', 'POST'])
def register():
    form = Registration()
    card_id = ReaderClass.read()
    if form.validate_on_submit():
        user = User(id=card_id, name=form.name, role=form.role)




    if request.method == 'POST':
        name = request.form["fullname"]
        role = request.form["role"]
        # def present_register():
        #     yield render_template('register.html')
        #     name = request.form("fullname")
        #     role = request.form("role")
        #     message = name + " " + role
        #     print(message)
        #     yield render_template('present_message.html', message=message)

        # return Response(stream_with_context(present_register()))
        print (name, " ", role)

    return render_template('register.html')

@app.route("/status")
def status():
    if request.method == 'GET':
        def present_status():
            yield render_template('status.html')
            reader_id, reader_name = ReaderClass.read("self")
            message = Command.get_status("self",reader_id,reader_name)
            yield render_template('present_message.html', action="status", message=message)
            time.sleep(30)
            yield render_template('home.html')
            ReaderClass.destroy("self")

        return Response(stream_with_context(present_status()))
    return render_template('status.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route("/clear", methods=['GET'])
def clear():
    if request.method == 'GET':
        ReaderClass.destroy("self")
        return redirect(url_for('home'))



