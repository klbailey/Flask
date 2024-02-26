from flask import Flask, render_template, request, redirect, url_for
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
        new_user = User(name=request.form['name'], email=request.form['email'])
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

# Route to delete static row
# @app.route('/confirm_delete_static', methods=['GET'])
# def confirm_delete_static():
#     return render_template('static_row_delete.html')

# Route to delete dynamic rows based on course_id parameter
# @app.route('/confirm_delete_dynamic/<int:course_id>', methods=['GET', 'POST'])
# def confirm_delete_dynamic(course_id):
#     course = Course.query.get_or_404(course_id)
#     if request.method == 'POST':
#         db.session.delete(course)
#         db.session.commit()
#         return redirect(url_for('index'))
#     return render_template('confirm_delete_dynamic.html', course=course, error=None)

# Initialize database tables w/create_all() & run on port 5000
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
