from bson.binary import Binary
import io
from flask import Blueprint, render_template, url_for, current_app, request, session
import time

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')


@patient_bp.route('/dashboard')
def dashboard():
    patient_data = current_app.db.patients.find_one(
        {'user_id': session['user_id']})

    if patient_data is None:
        return "No patient found", 404

    # Define the paths to your images
    image_paths = [url_for('static', filename='images/case-1.jpg'),
                   url_for('static', filename='images/case-2.png')]
    return render_template('patient_dash.html', patient=patient_data, image_paths=image_paths)


@patient_bp.route('/dashboard', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        filenames = ""

        for file in request.files.getlist("scans"):
            try:
                # upload the file to the container using the filename as the blob name
                if current_app.container_client is None:
                    print("bruh")

                print(current_app.container_client.get_container_properties())
                current_app.container_client.upload_blob(file.filename, file)

                filenames += file.filename + "<br /> "
            except Exception as e:
                print(e)
                # ignore duplicate filenames
                print("Ignoring duplicate filenames")

        return "<p>Uploaded: <br />{}</p>".format(filenames)
        # if 'scans' in request.files:
        #     # scan_images = request.files.getlist('scans')
        #     # scan_names = []

        #     filenames = ""

        #     for file in request.files.getlist("scans"):
        #         try:
        #             # upload the file to the container using the filename as the blob name
        #             current_app.container_client.upload_blob(
        #                 file.filename, file)
        #             filenames += file.filename + "<br /> "
        #         except Exception as e:
        #             print(e)
        #             # ignore duplicate filenames
        #             print("Ignoring duplicate filenames")

        #     return "<p>Uploaded: <br />{}</p>".format(filenames)

        # for file in request.files.getlist("scans"):
        #     try:
        #         # file.filename += patient_id
        #         current_app.container_client.upload_blob(
        #             file.filename, file)
        #         scan_names.append(file.filename)
        #     except Exception as e:
        #         print(e)
        #         # ignore duplicate filenames
        #         print("Ignoring duplicate filenames")

        # patient_id = session['user_id']
        # case_name = "case"
        # current_app.db.patients.update_one(
        #     {'patient_id': patient_id},
        #     {"$set": {"scans." + case_name: scan_names}},
        #     upsert=True)

        #     return "MRI scans uploaded and added to patient's case successfully!"
        # else:
        #     return "No MRI scans uploaded!", 400
