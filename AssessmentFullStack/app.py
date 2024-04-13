
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'secrets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctor.db'
db = SQLAlchemy(app)

# Define model class with fields
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())
    date = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)
    patient_name = db.Column(db.String(255), nullable=False)
    complaint = db.Column(db.Text, nullable=False)

# Home template to display existing appointments
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    else:
        username = session.get('username', None)
        appointments = Doctor.query.all()
        return render_template('index.html', username=username, appointments=appointments)

# Create new appointment in the database
@app.route('/add_appointment', methods=['POST'])
@app.route('/appointments', methods=['POST'])
def add_appointment():
    date = request.form.get('date')
    time = request.form.get('time')
    patient_name = request.form.get('patient_name')
    complaint = request.form.get('complaint')
    
    if not all([date, time, patient_name, complaint]):
        return 'Missing required fields', 400
    
    new_appointment = Doctor(date=date, time=time, patient_name=patient_name, complaint=complaint)
    db.session.add(new_appointment)
    db.session.commit()
    
    return redirect(url_for('index'))


@app.route('/add_appointment.html')
def add_appointment_page():
    return render_template('add_appointment.html')


# Add this route for deleting appointments
@app.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    appointment = Doctor.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()

    return redirect(url_for('index'))


# Initialize database tables and run the app
if __name__ == "__main__":
    if not os.path.exists('doctor.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True, port=5000)