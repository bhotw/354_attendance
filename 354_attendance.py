
from flask import Flask, render_template, request
from flask import Response, stream_with_context, redirect, url_for
from back_end.readerClass import ReaderClass
from back_end.command import Command
import time




app = Flask(__name__)



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
            time.sleep(3)
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
            time.sleep(3)
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

# @app.route("/present_info", methods=['GET', 'POST'])
# def present_info():
#     if request.method == 'GET':
#         data = session["getinfo"]
#         reader_id = data[0]
#         reader_name = data[1]
#         return render_template('present_message.html', reader_id=reader_id, reader_name=reader_name)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        def present_register():
            yield render_template('register.html')
            name = request.form("fullname")
            role = request.form("role")
            message = name + " " + role
            print(message)
            yield render_template('present_message.html', message=message)


        return Response(stream_with_context(present_register()))

@app.route("/status")
def status():
    if request.method == 'GET':
        def present_status():
            yield render_template('status.html')
            reader_id, reader_name = ReaderClass.read("self")
            message = Command.get_status("self",reader_id,reader_name)
            yield render_template('present_message.html', action="status", message=message)
            time.sleep(10)
            yield render_template('home.html')
            ReaderClass.destroy("self")

        return Response(stream_with_context(present_status()))
    return render_template('status.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')



if __name__ == "__main__":
    app.run(debug=True)