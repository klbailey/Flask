# app.py
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from form import RecipeForm, RegistrationForm, LoginForm, DeleteRecipeForm
from werkzeug.utils import secure_filename


import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define database models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='recipes', lazy=True)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create an instance of the LoginForm
    if form.validate_on_submit():  # Check if form is submitted and valid
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):  # Check if user exists and password is correct
            login_user(user)  # Log in the user
            flash('Logged in successfully.', 'success')
            return redirect(url_for('view_recipe'))  # Redirect to view_recipe page after successful login
        else:
            flash('Invalid username or password. Please register.', 'error')
            return redirect(url_for('register'))  # Redirect to register page if login fails
    return render_template('login.html', form=form)  # Pass the LoginForm object to the template


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Create an instance of the RegistrationForm
    if form.validate_on_submit():  # Check if form is submitted and valid
        username = form.username.data
        email = form.email.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))  # Redirect to register page if username already exists
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Set the password for the new user
        db.session.add(new_user)  # Add the new user to the database
        db.session.commit()  # Commit changes to the database
        login_user(new_user)  # Log in the newly registered user
        flash('Account created successfully. Welcome!', 'success')
        return redirect(url_for('view_recipe'))  # Redirect to view_recipe page after successful registration
    return render_template('register.html', form=form)  # Pass the RegistrationForm object to the template



@app.route('/view_recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        return render_template('view_recipe.html', recipe=recipe)
    else:
        # Handle case where recipe is not found
        return render_template('error.html', message='Recipe not found'), 404

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        ingredients = form.ingredients.data
        instructions = form.instructions.data

        # Check if an image file was uploaded
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                # Save the image file to the specified upload folder
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)

        # Create a new Recipe instance with the form data
        new_recipe = Recipe(title=title, description=description, ingredients=ingredients, instructions=instructions, image=filename, user=current_user)

        # Add the new recipe to the database
        db.session.add(new_recipe)
        db.session.commit()

        # Flash a success message
        flash('Recipe added successfully!', 'success')

        # Redirect to the view_recipe page
        return redirect(url_for('view_recipe'))

    # If the form is not submitted or is invalid, render the add_recipe template with the form
    return render_template('add_recipe.html', form=form)

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    # Retrieve the recipe from the database based on the provided recipe_id
    recipe = Recipe.query.get_or_404(recipe_id)

    # Create a form instance and populate it with the recipe data
    form = RecipeForm(obj=recipe)

    if form.validate_on_submit():
        # Update the recipe data based on the form submission
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data

        # Check if an image file was uploaded
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                # Save the image file to the specified upload folder
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                # Update the image attribute of the recipe with the new filename
                recipe.image = filename

        # Save the updated recipe to the database
        db.session.commit()

        # Redirect to the view_recipe page for the updated recipe
        return redirect(url_for('view_recipe', recipe_id=recipe.id))

    # If it's a GET request or the form is not valid, render the edit_recipe template
    return render_template('edit_recipe.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))



@app.route('/delete_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    # Retrieve the recipe from the database based on the provided recipe_id
    recipe = Recipe.query.get_or_404(recipe_id)
    form = DeleteRecipeForm()  # Create an instance of the DeleteRecipeForm
    if request.method == 'POST' and form.validate_on_submit():
        # Delete the recipe from the database
        db.session.delete(recipe)
        db.session.commit()

        # Redirect to the index page or any other appropriate page
        flash('Recipe deleted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('delete.html', recipe=recipe, form=form)





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

