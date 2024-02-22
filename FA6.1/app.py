from flask import Flask, render_template, session

app = Flask(__name__)
app.secret_key = 'ThisIsSecret'

@app.route("/")
def index():
    if "counter" not in session:
        session["counter"] = 0
    else:
        session["counter"] += 1
    return render_template("index.html", counter=session["counter"])

@app.route("/addtwo")
def addtwo():
    if "counter" not in session:
        session["counter"] = 2
    else:
        session["counter"] += 2
    return render_template("index.html", counter=session["counter"])

@app.route("/reset")
def reset():
    session["counter"] = 0
    return render_template("index.html", counter=session["counter"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
