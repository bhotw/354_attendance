from flask import Flask, render_template

app = Flask(__name__)


@app.route("/home")
def home():
    return render_template('home.html')
@app.route("/status")
def status():
    return render_template('status.html')

@app.route("/")
def hello_world():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(Debug=True)