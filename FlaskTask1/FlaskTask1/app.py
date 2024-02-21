# implement the views for the ‘home’ and ‘about’ pages
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") 
# Home page should output string
def homePage():
    return "Paws Rescue Center 🐾"

# About page
@app.route("/about")
def aboutPage():     
    return 'We are a non-profit organization working as an animal rescue. We aim to help you connect with the purrfect furbaby for you! The animals you find on our website are rescued and rehabilitated animals. Our mission is to promote the ideology "adopt, don\'t shop"!'

if __name__ == "__main__":
    app.run(debug = True, port = 5000)