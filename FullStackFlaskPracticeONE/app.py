from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
# import forms import RegistrationForm, LoginForm
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# Set secret key
app.config['SECRET_KEY'] = 'secret'

# Set config variable so app knows where database is; using SQLite sqlite:///filename
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Complete initialization (instance) create object of SQLAlchemy class; we have to provide our
# appliation as a parameter to its constructor
db = SQLAlchemy(app)

# Create a model class for User/Add columns for table(email,password)
# Each column will be an objet of the Column subclass of SQLAlchemy
# Here we use string but others allowed are Integer,String(size),Text,DateTime,Float,
# Boolean,PickleType,LargeBinary. Optional params primary_key,nullable,unique,index
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(40), unique=False, nullable=False)
    lastName = db.Column(db.String(40), unique=False, nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #post attribute has relationship to post model; backref like adding another column
    #when we have a post we can use author attribute to get user who created post
    #lazy defines when SQLAlchemy loads the data from the dataabase in one go
    posts = db.relationship('Post', backref='author', lazy=True)
    # repr method how our object is printed whenever we print it out
    def __repr__(self):
        return f"User('{self.firstName}', '{self.lastName}', '{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # id of user who authored post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # repr method how our object is printed whenever we print it out
    def __repr__(self):
        return f"Post('{self.title}', '{self.datePosted}')"

# Initialize database within the app context for proper handling of database sessions
# The model just created will be created in database

print("creating tables...")
with app.app_context():
    db.create_all()
print("Tables created")

# List of dictionaries each dictionary represents blog post
posts = [
    {
        'author': 'Sansa Stark',
        'title': "I'm a slow learner, it's true. But I learn.",
        'content': 'First post content',
        'datePosted': 'February 22, 2024'
    },
    {
        'author': 'Jon Snow',
        'title': 'Winter is coming',
        'content': 'Second post content',
        'datePosted': 'February 23, 2024'
    }
]

@app.route('/')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

# Registration Route
@app.route('/register', methods =['GET', 'POST'])
def register():
    # Create an instance of form
    form = RegistrationForm()
    # Check to see if post data is valid for the form using flash message/alert
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        #direct to new page
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# Login Route
@app.route('/login', methods =['GET', 'POST'])
def login():
    # Create an instance of form
    form = LoginForm()
    # Check to see if data is valid for the form using flash message/alert
    if form.validate_on_submit():
        if form.username.data == 'admin@blog.com' and form.password.data == "password":
           flash(f"Welcome {form.username.data}!", 'success')
           return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful Check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

# New route to query the database
@app.route('/view_users')
def view_users():
    users = User.query.all()
    for user in users:
        print(user)
    return 'Check your terminal for the list of users.'

# New route to query the database for posts
@app.route('/view_posts')
def view_posts():
    posts = Post.query.all()
    for post in posts:
        print(post)
    return 'Check your terminal for the list of posts.'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
