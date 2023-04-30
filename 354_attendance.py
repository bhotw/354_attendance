
from flask import Flask, render_template, request
from flask import Response, stream_with_context, redirect
from back_end.readerClass import ReaderClass
from back_end.command import Command




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
            # message = Command.sign_in("self",reader_id,reader_name )
            message = "Id: "+reader_id + "name:" + reader_name+"You have singed out at:" + ReaderClass.get_time("self")  # just for testing
            yield render_template('present_message.html', action="sign_in", message=message)
        return render_template(stream_with_context(present_sign_in()))

@app.route("/sign_out", methods=['GET', 'POST'])
def sign_out():

    if request.method == 'GET':
        def present_sign_out():
            yield render_template('sign_out.html')
            reader_id, reader_name = ReaderClass.read("self")
            # message = Command.sign_out(reader_id, reader_name)
            message = "Id: "+reader_id + "name:" + reader_name+"You have singed out at:" + ReaderClass.get_time("self")  # just for testing
            yield render_template('present_message.html', action="sign_out", message=message)

        return render_template(stream_with_context(present_sign_out()))


@app.route("/get_info", methods=['GET', 'POST'])
def get_infor():
    if request.method == 'GET':

        def present_info():
            yield render_template('get_info.html')
            reader_id, reader_name = ReaderClass.read("self")
            data = [reader_id, reader_name]
            yield render_template('present_message.html', action="info", reader_id=reader_id, reader_name=reader_name)
        return Response(stream_with_context(present_info()))

# @app.route("/present_info", methods=['GET', 'POST'])
# def present_info():
#     if request.method == 'GET':
#         data = session["getinfo"]
#         reader_id = data[0]
#         reader_name = data[1]
#         return render_template('present_message.html', reader_id=reader_id, reader_name=reader_name)

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/status")
def status():
    if request.method == 'GET':
        def present_status():
            yield render_template('status.html')
            reader_id, reader_name = ReaderClass.read("self")
            message = Command.get_status(" ",reader_id,reader_name)
            print("this is inside status",message)
            yield render_template('present_message.html', action="status", message=message)

        return Response(stream_with_context(present_status()))
    return render_template('status.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')



if __name__ == "__main__":
    app.run(debug=True)