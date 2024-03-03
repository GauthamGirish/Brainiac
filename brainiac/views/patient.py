from flask import Blueprint, render_template, url_for, current_app

patient_bp = Blueprint('patient', __name__ , url_prefix='/patient')

@patient_bp.route('/dashboard')
def dashboard():
    patient_data = current_app.db.patients.find_one()

    if patient_data is None:
        return "No patient found", 404

    #Define the paths to your images
    image_paths = [url_for('static', filename='images/case-1.jpg'),
                   url_for('static', filename='images/case-2.png')]
    return render_template('patient_dash.html', patient=patient_data, image_paths=image_paths)
