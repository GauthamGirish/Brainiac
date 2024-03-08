#I've just added some boilerplate code to check if the redirects are working properly

from flask import Blueprint, render_template, url_for, current_app, session, redirect, request

doctor_bp = Blueprint('doctor', __name__ , url_prefix='/doctor')

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
            image_urls[patient_id, case_number] = patient_data["scans"]['case' + str(case_number)]
    #just a fallback image for now - G
    else:
        image_urls["Agent J"] = ['https://brainiac02.blob.core.windows.net/mriscans/WhatsApp Image 2023-03-23 at 7.12.19 PM.jpeg']
    
    return render_template('doctor_dash.html', doctor=doctor_data, cases=image_urls)

@doctor_bp.route('/view_case/<int:patient_id>/<int:case_number>')
def view_case(patient_id, case_number):
    if session.get('user_id', default=None) is None:
        return redirect(url_for("auth.login"))
    patient_data = current_app.db.patients.find_one({'user_id': patient_id})
    image_urls = patient_data["scans"]['case' + str(case_number)]
    return render_template('case.html', patient_data=patient_data, case_number=case_number,
                           image_urls=image_urls, user_id=session['user_id'])

@doctor_bp.route('/edit-details', methods = ['POST'])
def edit():
    if session.get('user_id', default=None) is None:
        return redirect(url_for("auth.login"))

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    gender = request.form.get('gender')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    address = request.form.get('address')
    birthday = request.form.get('birthday')
    current_app.db.doctors.update_one(
        {"user_id": session['user_id']},
        {
            "$set": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": phone_number,
                "address": address,
                "gender": gender,
                "birthday": birthday
            },
        }
    )
    return redirect(url_for('doctor.dashboard'))