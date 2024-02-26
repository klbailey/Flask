from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

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

# Route to delete static row
@app.route('/confirm_delete_static', methods=['GET'])
def confirm_delete_static():
    return render_template('static_row_delete.html')

# Route to delete dynamic rows
@app.route('/confirm_delete_dynamic/<int:course_id>', methods=['GET', 'POST'])
def confirm_delete_dynamic(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('confirm_delete_dynamic.html', course=course, error=None)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
