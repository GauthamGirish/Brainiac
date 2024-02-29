from flask import Blueprint

patient = Blueprint('patient', __name__)


@patient.route('/dashboard')
def dashboard():
    return '<h1>Patient Dash</h1>'