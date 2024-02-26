from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
# migrate = Migrate(app, db)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/add_course', methods=['POST'])
def add_course():
    if request.method == 'POST':
        new_course = Course(name=request.form['name'], description=request.form['description'])
        db.session.add(new_course)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('home.html', courses=Course.query.all())

# Route to delete 
@app.route('/confirm_delete/<int:course_id>', methods=['GET', 'POST'])
def confirm_delete(course_id):
    course = Course.query.get_or_404(course_id)
    print(course)  # Add this line to print the value of course
    if request.method == 'POST':
        # Handle the deletion here if the user clicks "Yes"
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('confirm_delete.html', course=course, error=None)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
