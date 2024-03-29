from flask import Flask, render_template
from forms import LoginForm
# Create database connection
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
# Set config variable so app knows where database is; using SQLite sqlite:///filename
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'

# Complete initialization create object of SQLAlchemy class; we have to provide our
# appliation as a parameter to its constructor
db = SQLAlchemy(app)

# Create a model class for User/Add columns for table(email,password)
# Each column will be an objet of the Column subclass of SQLAlchemy
# Here we use string but others allowed are Integer,String(size),Text,DateTime,Float,
# Boolean,PickleType,LargeBinary. Optional params primary_key,nullable,unique,index
# Here primary_key=True indicates it is primary key of table
class User(db.Model):
    email = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

# The model just created will be created in database
db.create_all()

users = {
    "archie.andrews@email.com": "football4life",
    "veronica.lodge@email.com": "fashiondiva"
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        for u_email, u_password in users.items():
            if u_email == form.email.data and u_password == form.password.data:
                return render_template("login.html", message ="Successfully Logged In")
        return render_template("login.html", message ="Incorrect Email or Password")

    elif form.errors:
        print(form.errors.items())

    return render_template("login.html", form = form)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=3000)