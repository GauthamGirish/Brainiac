from flask import Blueprint, render_template, current_app, request, session, redirect, url_for
from . import tasks

patient_bp = Blueprint("patient", __name__, url_prefix="/patient")


@patient_bp.route("/dashboard")
def dashboard():
    if session.get('user_id', default=None) is None:
        return redirect(url_for("auth.login"))

    patient_data = current_app.db.patients.find_one({'user_id': session['user_id']})
    return render_template('patient_dash.html', patient=patient_data)


@patient_bp.route("/dashboard", methods=["POST"])
def upload_image():
    if request.method == "POST":
        scan_names = []
        img_urls = []

        patient_id = session["user_id"]
        patient_data = current_app.db.patients.find_one(
            {"user_id": patient_id})

        img_count = 1
        case_count = 1

        # check if case number exists
        if "case_number" in patient_data:
            case_count = patient_data["case_number"] + 1

        # update azure
        for scan in request.files.getlist("scans"):
            try:
                # rename scan
                new_scan_name = "patient" + \
                    str(patient_id) + "_" + "case" + \
                    str(case_count) + "_" + "img" + str(img_count)
                img_count += 1
                scan_names.append(new_scan_name)

                # upload image and get url
                blob_client = current_app.container_client.get_blob_client(new_scan_name)
                print("blob client setup")
                current_app.container_client.upload_blob(new_scan_name, scan)
                print("blob uploaded")
                img_urls.append(blob_client.url)
            except Exception as e:
                print(e)
                print("Ignoring duplicate filenames")

        # update mongodb
        case_name = "case" + str(case_count)
        current_app.db.patients.update_one(
            {"user_id": patient_id},
            {
                "$inc": {"case_number": 1},
                "$set": {"case_details." + case_name: {"status": "Processing", "scans": img_urls}}
            }
        )

        # passing necessary data to dl model
        tasks.process_case(patient_data, case_count, img_urls)

        return redirect(url_for('patient.dashboard'))


@patient_bp.route('/edit-details', methods=['POST'])
def edit():
    if session.get('user_id', default=None) is None:
        return redirect(url_for("auth.login"))

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    gender = request.form.get('gender')
    email_id = request.form.get('email_id')
    phone_number = request.form.get('phone_number')
    address = request.form.get('address')
    birthday = request.form.get('birthday')

    current_app.db.patients.update_one(
        {"user_id": session['user_id']},
        {
            "$set": {
                "first_name": first_name,
                "last_name": last_name,
                "email_id": email_id,
                "phone_number": phone_number,
                "address": address,
                "gender": gender,
                "birthday": birthday
            },
        }
    )

    return redirect(url_for('patient.dashboard'))
