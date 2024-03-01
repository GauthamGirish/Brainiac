from flask import Blueprint, render_template

patient = Blueprint('patient', __name__, template_folder='../templates/patient')

@patient.route('/dashboard')
def dashboard():
    return render_template('patient_dashboard.html')
