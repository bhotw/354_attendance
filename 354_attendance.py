from flask import Flask

app = Flask(__name__)

@app.route("/home")
def home():
    return 'home'
@app.route("/status")
def status():
    return 'status'

@app.route("/")
def hello_world():
    return "<p> Hello, World! </p>"