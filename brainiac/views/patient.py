from flask import Blueprint, render_template, url_for
from database import db

patient = Blueprint('patient', __name__,
                    template_folder='../templates/patient')


@patient.route('/dashboard')
def dashboard():
    patient_data = db.patients.find_one()

    if patient_data is None:
        return "No patient found", 404

    # Define the paths to your images
    image_paths = [url_for('static', filename='images/case-1.jpg'),
                   url_for('static', filename='images/case-2.png')]
    return render_template('patient_dashboard.html', patient=patient_data, image_paths=image_paths)
