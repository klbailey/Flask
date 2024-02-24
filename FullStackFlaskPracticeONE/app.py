from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
# import forms import RegistrationForm, LoginForm
from forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import logout_user, login_user, current_user, LoginManager, login_required
import secrets
from PIL import Image # to import 'image' modeul
import os #to keep site.db in this project folder

app = Flask(__name__)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Set secret key
app.config['SECRET_KEY'] = 'secret'

# Set config variable so app knows where database is; using SQLite sqlite:///filename
# Specify the absolute path to the instance folder and site.db file
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
db_path = os.path.join(instance_path, 'site.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'


# Set config variable for upload folder
app.config['UPLOAD_FOLDER'] = os.path.join('path', 'to', 'your', 'upload', 'folder')

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
    #lazy defines when SQLAlchemy loads the data from the database in one go
    posts = db.relationship('Post', backref='author_posts', lazy=True)
    # repr method how our object is printed whenever we print it out
    def __repr__(self):
        return f"User('{self.firstName}', '{self.lastName}', '{self.username}', '{self.email}', '{self.image_file}')"
    # Flask-Login methods
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
# Add user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # id of user who authored post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Add the relationship to the User model to access user information
    author = db.relationship('User', backref='author_posts', lazy=True)

    # repr method how our object is printed whenever we print it out
    def __repr__(self):
        return f"Post('{self.title}', '{self.datePosted}')"

# Initialize database within the app context for proper handling of database sessions
# The model just created will be created in database
# with app.app_context():
#     db.create_all()


# List of dictionaries each dictionary represents blog post
posts = [
    {
        'author': 'Sansa Stark',
        'title': "I'm a slow learner, it's true. But I learn.",
        'content': '''Sometimes when I'm trying to understand a person's motives, I play a little game... 
            I assume the worst. What's the worst reason you'd have for turning me against my sister? That's 
            what you do, isn't it, that's what you've always done - you turn family against family, you turn 
            sister against sister; that's what you did to our mother and Aunt Lysa, and that's what you tried 
            to do to us. ''',
        'datePosted': 'February 22, 2024'
    },
    {
        'author': 'Jon Snow',
        'title': "Winter is coming",
        'content': "We know what's coming with it. We can learn to live with the wildlings, or we can add them to the army of the dead.",
        'datePosted': 'February 23, 2024'
    }
]

@app.route('/')
def home():
    # Get the newly created user id from the URL parameters
    new_user_id = request.args.get('new_user_id')
    new_user = None
    
    if new_user_id:
        # Retrieve the user from the database based on the ID
        new_user = User.query.get(new_user_id)

    # Instantiate the PostForm
    post_form = PostForm()

     # Only allow the form to be displayed for logged-in users
    if current_user.is_authenticated:
        if post_form.validate_on_submit():
            # Create a new Post instance with data from the form
            new_post = Post(
                title=post_form.title.data,
                content=post_form.content.data,
                author=current_user  # Assuming the current user is logged in
            )
            db.session.add(new_post)
            db.session.commit()

            flash('Your post has been created!', 'success')

    # Retrieve the latest posts from the database
    posts = Post.query.order_by(Post.datePosted.desc()).all()

    return render_template('home.html', posts=posts, new_user=new_user, post_form=post_form)

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
        # Create a new User instance with data from the form
        new_user = User(
            firstName=form.firstName.data,
            lastName=form.lastName.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        
        # Retrieve the ID of the newly created user
        new_user_id = new_user.id

        #direct to new page with newly created user id data
        return redirect(url_for('home', new_user_id=new_user.id))
    
    return render_template('register.html', title='Register', form=form)

# Login Route
@app.route('/login', methods =['GET', 'POST'])
def login():
    # Create an instance of form
    form = LoginForm()
    # Check to see if data is valid for the form using flash message/alert
    if form.validate_on_submit():
        # Query the database to find a user with the provided username
        user = User.query.filter_by(username=form.username.data).first()
        # Check if the user exists and if the password is correct
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            flash(f"Welcome {form.username.data}!", 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Check username and password.', 'danger')
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

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# User can update on Account page, gets message, and it's saved to database
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        # Update the user's account information in the database
        current_user.firstName = form.firstName.data
        current_user.lastName = form.lastName.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        # Handle profile picture update
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        # Pre-fill the form with the current user's information
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.username.data = current_user.username
        form.email.data = current_user.email

    # image and concatenate current user image
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)

# Update Account Route
@app.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        # Update the user's account information in the database
        current_user.firstName = form.firstName.data
        current_user.lastName = form.lastName.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        # Handle profile picture update
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        # Pre-fill the form with the current user's information
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('update_account.html', title='Update Account', form=form)

# /pip install Pillow
def save_picture(form_picture):
    # Generate a unique filename to avoid overwriting existing files
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Resize the image before saving (optional, you can skip this step)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn

@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    post_form = PostForm()

    if post_form.validate_on_submit():
        new_post = Post(title=post_form.title.data, content=post_form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')

    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5000)
