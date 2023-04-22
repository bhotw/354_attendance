from flask import Flask, render_template

app = Flask(__name__)


@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/sign_in")
def sign_in():
    return render_template('sign_in.html')

@app.route("/sign_out")
def sign_out():
    return render_template('sign_out.html')
@app.route("/get_info")
def get_infor():
    return render_template('get_info.html')
@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/status")
def status():
    return render_template('status.html')



if __name__ == "__main__":
    app.run(debug=True)