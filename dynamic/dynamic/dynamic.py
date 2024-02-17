'''An example application to demonstrate Variable Rules in Routing
from flask import Flask
app = Flask(__name__)
@app.route("/")
def home():
"""View for the Home page of the website."""
    return "Welcome to the HomePage!"

@app.route("/<my_name>")

#varialbe rule /<my_name> my_name is variable passed as parameter to greetings() and then returned
def greatings(my_name):
"""View function to greet the user by name."""
    return "Welcome "+ my_name +"!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)'''

"""An example application to demonstrate Dynamic Routing"""
#http://127.0.0.1:3000/square/5 in url
from flask import Flask

app = Flask(__name__)

@app.route("/")

def home():
#View for the Home page of the Website
    return "Welcome to the HomePage!"

@app.route('/square/<int:number>')
def show_square(number):
#View that shows the square of the number passed by URL
    return "Square of "+ str(number) +" is: "+ str(number * number)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)