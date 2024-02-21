from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Set a secret key for session security
app.secret_key = 'secret_key'  

# Root URL GET renders form.html, POST stores form data in session/redirects to display_data endpoint.
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data and STORES it in session
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        session['favorite_food'] = request.form['favorite_food']
        
        # After STORING, redirect to a separate page to display the submitted data
        return redirect(url_for('display_data'))

    return render_template('form.html')

# The data remains in the session until the session is cleared or times out
@app.route('/display_data')
def display_data():
    # Retrieve STORED data from session
    first_name = session.get('first_name', '')
    last_name = session.get('last_name', '')
    email = session.get('email', '')
    favorite_food = session.get('favorite_food', '')
    # Render STORED data from session soe if user refreshes page or access display_data again,
    # data is still present in session and user continues to see their info
    return render_template('display_data.html', first_name=first_name, last_name=last_name, email=email, favorite_food=favorite_food)

if __name__ == '__main__':
    app.run(debug=True, port = 3000)


