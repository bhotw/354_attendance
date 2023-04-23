from flask import Flask, render_template, request
from back_end.readerClass import ReaderClass

app = flask.Flask(__name__)


@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    return render_template('sign_in.html')

@app.route("/sign_out")
def sign_out():

    return render_template('sign_out.html')
@app.route("/get_info", methods=['GET', 'POST'])
def get_infor():
    while True:
        if request.method == 'GET':
            reader_id, reader_name = ReaderClass.read("self")
            rendered = flask.render_template('get_info.html')
@app.route("/present_info")
def present_info():
    if request.method == 'GET':
        reader_id, reader_name = ReaderClass.read("self")
        return render_template('present_info.html', reader_id=reader_id, reader_name=reader_name )

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/status")
def status():
    return render_template('status.html')



if __name__ == "__main__":
    app.run(debug=True)