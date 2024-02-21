from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
# Set a secret key for session security
app.secret_key = 'mysecretkey'

# https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/
# https://stackoverflow.com/questions/52620992/how-can-i-make-a-non-permanent-session-in-flask

@app.route('/')
def index():
    session['counter'] = session.get('counter', 0)
    return render_template('index.html', counter=session['counter'])
    # if "counter" not in session:
    #     session["counter"] = 0
    # else:
    #     session["counter"] = session["counter"] + 1
    # return render_template("index.html")

@app.route('/addTwo', methods=['POST'])
def addTwo():
    session['counter'] += 2
    session.modified = True
    return redirect(url_for('index'))
    # if "counter" not in session:
    #     session["counter"] = 2
    # else:
    #     session["counter"] += 2
    # return render_template("index.html")

@app.route('/reset', methods=['POST'])
def reset():
    if request.method == 'POST':
        session['counter'] = 0
        session.modified = True
    return redirect(url_for('index'))
    # session["counter"] = 0
    # return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)