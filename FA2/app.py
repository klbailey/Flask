from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Render an HTML page that prints out myInfo in h1 tags:
# @app.route('/')
# def home():
#     return '''
#     <h1>First Name:  Kathy<br>
#         Last Name:  Bailey Hines<br>
#         Favorite Food:  Seafood<br>
#         Favorite Vacation Destination:  Ocean
#     </h1> '''

@app.route('/')
def index():
    myInfo = {
        'firstName': 'Kathy',
        'lastName': 'Bailey Hines',
        'favoriteFood': 'Seafood',
        'favoriteDestination': 'Ocean'
    }
    return render_template('index.html', myInfo=myInfo)

# Decorator defining a route for '/submit' that responds to POST requests.
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    email = request.form.get('email')
    favoriteFood = request.form.get('favoriteFood')

    # Create a dictionary to pass to the template
    formData = {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'favoriteFood': favoriteFood
    }

    # Get separate HTMl page with submitted data
    return render_template('formSubmit.html', formData=formData)

if __name__ == '__main__':
    app.run(debug = True, port = 5000)