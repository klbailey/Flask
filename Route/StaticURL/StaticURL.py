from flask import Flask, render_template
app = Flask(__name__)

# home() view corresponds to route "/" It's default route of any web app
@app.route("/")
def home():
    return "Welcome to the HomePage!"

# learn() view corresponds to route "/educative"
@app.route("/educative")

def learn():
    return "Happy Learning at Educative!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)