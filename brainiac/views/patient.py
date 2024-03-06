from flask import Blueprint, render_template, current_app, request, session, redirect, url_for

patient_bp = Blueprint("patient", __name__, url_prefix="/patient")


@patient_bp.route("/dashboard")
def dashboard():

    patient_data = current_app.db.patients.find_one({'user_id': session['user_id']})

    if patient_data is None:
        return redirect(url_for("auth.login"))

    if "scans" in patient_data:
        # Retrieve image URLs from the MongoDB document
        print(patient_data['scans'])
        return render_template('patient_dash.html', patient=patient_data, cases=patient_data['scans'])
    else:
        return render_template('patient_dash.html', patient=patient_data, cases={})


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
                blob_client = current_app.container_client.get_blob_client(
                    new_scan_name)
                current_app.container_client.upload_blob(new_scan_name, scan)
                img_urls.append(blob_client.url)
            except Exception as e:
                print(e)
                print("Ignoring duplicate filenames")

        # update mongodb
        case_name = "case" + str(case_count)
        current_app.db.patients.update_one(
            {"user_id": patient_id},
            {
                "$set": {"scans." + case_name: img_urls},
                "$inc": {"case_number": 1}
            }
        )
        return redirect(url_for('patient.dashboard'))
