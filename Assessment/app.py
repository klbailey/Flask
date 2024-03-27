from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "123"

@app.route("/") 
# Home page
def homePage():
    return render_template("home.html", title="Home")

@app.route("/about")
# About page
def aboutPage():
    return render_template("about.html", title="About")

# Index.html display welcome message with user's first name
@app.route("/greet/<name>")
def greet(name):
    return render_template("index.html", firstName=name)

# Contact form HTML page
@app.route("/contact")
def contact():
    return render_template("form.html")

# get and submit contact
@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        phone = request.form.get("phone")
        address = request.form.get("address")
        state = request.form.get("state")
        zipcode = request.form.get("zipcode")

        # Validate form data
        if not (firstname and lastname and phone and address and state and zipcode):
            return render_template("contact_error.html")
        # Display submission on confirmation page
        return render_template("contact_confirmation.html", firstname=firstname, lastname=lastname, phone=phone, address=address, state=state, zipcode=zipcode)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check if username and password match
        if username == "admin" and password == "password":
            # Store user's login status in session
            session["logged_in"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("login.html", message="Invalid username or password")

    # Render the login form
    return render_template("login.html", message=None)

@app.route("/admin")
def admin():
    # Check if user is logged in
    if session.get("logged_in"):
        logged_in_status = "User is logged in."
    else:
        logged_in_status = "User is not logged in."

    return render_template("admin.html", logged_in_status=logged_in_status)
if __name__ == "__main__":
    app.run(debug = True, port = 5000)