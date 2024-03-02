from flask import Blueprint, render_template
from database import db

patient = Blueprint('patient', __name__,
                    template_folder='../templates/patient')


@patient.route('/dashboard')
def dashboard():
    patient_data = db.patients.find_one()
    if patient_data is None:
        return "No patient found", 404

    return render_template('patient_dashboard.html', patient=patient_data)
