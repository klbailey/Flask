from flask import Flask, render_template, request, redirect, url_for

# Constructor
app = Flask(__name__)

# Root Endpoint
@app.route('/', methods=['GET'])
def index():
    # Display HTML form template
    return render_template('index.html')

# Read endpoint
@app.route('/readForm', methods=['POST'])
def readForm():
    # Get form data as Python datatype
    data = request.form
    # Return extracted info
    return render_template('index.html', user_data=data)

# Submit endpoint
@app.route('/submit', methods=['GET'])
def submit():
    # Get form data using request.args as it's redirected with data
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    email = request.args.get('email')
    homeAddress = request.args.get('homeAddress')
    userCity = request.args.get('userCity')
    userState = request.args.get('userState')
    country_state = request.args.get('country-state')
    userZip = request.args.get('userZip')
    gender= request.args.get('gender')

    return render_template('index.html', user_data={
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'homeAddress': homeAddress,
        'userCity': userCity,
        'userState': userState,
        'country_state': country_state,
        'userZip': userZip,
        'gender': gender
    })

                                
# Main Driver Function
if __name__ == '__main__':
    # Run on local server
    app.run(debug = True, port = 5000)