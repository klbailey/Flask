from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") 
# Home page
def homePage():
    return render_template("home.html", title="Home")

# About page
@app.route("/about")
def aboutPage():     
    return render_template("about.html", title="About")

if __name__ == "__main__":
    app.run(debug = True, port = 5000)