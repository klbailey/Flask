from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import os #to keep site.db in this project folder

# Initialize and configure
app = Flask(__name__)
# Set config variable so app knows where database is; using SQLite sqlite:///filename
# Specify the absolute path to the instance folder and site.db file
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
db_path = os.path.join(instance_path, 'site.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

# Define model class with fields
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

# Handle post request to add new user to database via form
# from add_user.html form submitted via post to /users/create
@app.route('/users/create', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        # Get first and last names from the form
        first_name = request.form['name']
        last_name = request.form['lname']
        email = request.form['email']
         # Create a new user instance with first and last names
        new_user = User(name=f"{first_name} {last_name}", email=email)
        db.session.add(new_user)
        db.session.commit()
        #for debugging
        print("User added successfully")
        return redirect(url_for('index'))
    return render_template('add_user.html')

# Render home template w/list of users retrieved from database
@app.route('/')
def index():
    users = User.query.all()
    print("Number of users:", len(users))
    return render_template('home.html', users=users)

# User Show
@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

# User Edit
@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        # If it's a POST request, handle the form submission and update the user
        updated_first_name = request.form['name']
        updated_last_name = request.form['lname']
        updated_email = request.form['email']

        # Update user's information
        user.name = f"{updated_first_name} {updated_last_name}"
        user.email = updated_email

        # Commit changes to the database
        db.session.commit()

        print("User updated successfully")

        return redirect(url_for('index'))

    # If it's a GET request, render the edit_details.html template
    return render_template('edit_details.html', user=user)


# User Update
@app.route('/users/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        # Get updated information from the form
        updated_first_name = request.form['name']
        updated_last_name = request.form['lname']
        updated_email = request.form['email']

        # Update user's information
        user.name = f"{updated_first_name} {updated_last_name}"
        user.email = updated_email

        # Commit changes to database
        db.session.commit()

        print("User updated successfully")

        return redirect(url_for('index'))

    # Render edit_details.html template if request method is not POST
    return render_template('edit_details.html', user=user)

# User Delete Confirmation
@app.route('/users/delete/<int:user_id>')
def confirm_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('confirm_delete_user.html', user=user)

# User Delete
@app.route('/users/delete/<int:user_id>/confirmed', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Delete the user
        db.session.delete(user)
        db.session.commit()

        print("User deleted successfully")

        return redirect(url_for('index'))

    # If it's not a POST request, show an error
    abort(405)  # Method Not Allowed


# Initialize database tables w/create_all() & run on port 5000
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
