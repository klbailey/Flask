from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") 
# Home page
def homePage():
    pets = [
    {"id": "frenchie", "name": "Nelly", "age": "5 weeks", "bio": "I am a handsome dog of the superior breed."},
    {"id": "engbulldog", "name": "Ophelia", "age": "6 years", "bio": "I am a champion."},
    {"id": "frbulldog", "name": "Rodney", "age": "6 years", "bio": "I am the best dog on the planet, ever."}
    ]
    return render_template("home.html", title="Home", pets=pets)

# About page
@app.route("/about")
def aboutPage():     
    return render_template("about.html", title="About")

if __name__ == "__main__":
    app.run(debug = True, port = 5000)