from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed

# Create an app that takes in your first name, last name, 
# username, e-mail and a password via form submission.
# Command: pip install flask-wtf (forms)

class RegistrationForm(FlaskForm):
    # Form fields string field with validators(required/min and max amount)
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

# Add a login field to your app that searches your database for the correct username and password.
class LoginForm(FlaskForm):
    # Form fields string field with validators(required/min and max amount)
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=15)])
    password = PasswordField('Password', validators=[InputRequired()])
    # Boolean field (True or False)
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# User can update account 
class UpdateAccountForm(FlaskForm):
    # Form fields string field with validators(required/min and max amount)
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    # password = PasswordField('Password', validators=[InputRequired()])
    # confirm_password = PasswordField('Confirm Password', 
    #                                  validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Update')

# New form to create post
class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])
    submit = SubmitField('Post')

    
class UpdatePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')
