from bson.binary import Binary
import io
from flask import Blueprint, render_template, url_for, current_app, request

patient = Blueprint('patient', __name__, url_prefix='/patient')


@patient.route('/dashboard')
def dashboard():
    patient_data = current_app.db.patients.find_one()

    if patient_data is None:
        return "No patient found", 404

    # Define the paths to your images
    image_paths = [url_for('static', filename='images/case-1.jpg'),
                   url_for('static', filename='images/case-2.png')]
    return render_template('patient_dash.html', patient=patient_data, image_paths=image_paths)


@patient.route('/dashboard', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        if 'mri_scan' in request.files:
            mri_scan = request.files['mri_scan']
            mri_scan_in_memory = io.BytesIO()
            mri_scan.save(mri_scan_in_memory)
            mri_scan_in_memory.seek(0)
            mri_scan_binary = Binary(mri_scan_in_memory.read())

            current_app.db.cases.insert_one(
                {'mri_scan': mri_scan_binary})
            return "MRI scan uploaded and added to patient's case successfully!"
        else:
            return "No MRI scan uploaded!", 400
