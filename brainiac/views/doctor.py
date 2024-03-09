# I've just added some boilerplate code to check if the redirects are working properly

from flask import Blueprint, render_template, url_for, current_app, session, redirect, request

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')


@doctor_bp.route('/dashboard')
def dashboard():
    if session.get('user_id', default=None) is None:
        return redirect(url_for("auth.login"))

    doctor_data = current_app.db.doctors.find_one({'user_id': session['user_id']})

    if doctor_data is None:
        return redirect(url_for('auth.login'))

    image_urls = {}

    if "cases" in doctor_data:
        for case in doctor_data["cases"]:
            patient_id, case_number = case
            patient_data = current_app.db.patients.find_one({'user_id': patient_id})
            image_urls[patient_id, case_number] = patient_data["case_details"]['case' + str(case_number)]["scans"]

    return render_template('doctor_dash.html', doctor=doctor_data, cases=image_urls)


@doctor_bp.route('/view_case/<int:patient_id>/<int:case_number>', methods=['GET', 'POST'])
def view_case(patient_id, case_number):
    if session.get('user_id', default=None) is None:
        return redirect(url_for("auth.login"))
    
    if request.method == 'POST':
        patient_data = current_app.db.patients.find_one({'user_id': patient_id})
        treatment = request.form.get('treatment')
        diagnosis = request.form.get('diagnosis')
        case_name = "case" + str(case_number)
        current_app.db.patients.update_one(
            {"user_id": patient_id},
            {
                "$set": {"case_details." + case_name + ".treatment": treatment, 
                         "case_details." + case_name + ".diagnosis": diagnosis}
            }
        )

    patient_data = current_app.db.patients.find_one({'user_id': patient_id})
    return render_template('case.html', patient_data=patient_data, case_number=case_number, user_id=session['user_id'])


@doctor_bp.route('/edit-details', methods=['POST'])
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
    current_app.db.doctors.update_one(
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
    return redirect(url_for('doctor.dashboard'))
