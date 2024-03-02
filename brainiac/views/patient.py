from flask import Blueprint

patient_bp = Blueprint('patient', __name__ , url_prefix='/patient')


@patient_bp.route('/dashboard')
def dashboard():
    return '<h1>Patient Dash</h1>'