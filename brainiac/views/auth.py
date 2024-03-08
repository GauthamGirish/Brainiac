from flask import Blueprint, redirect, render_template, request, session, url_for, current_app

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email_id = request.form['email_id']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        birthday = request.form['birthday']
        gender = request.form['gender']
        role = request.form['role']

        if role == 'patient':
            existing_user = current_app.db.patients.find_one({'$or': [{'email_id': email_id}, {'phone_number': phone_number}]})
            if existing_user is not None:
                return render_template('register.html', message="User already exists")
            user_id = current_app.db.meta.find_one_and_update({'field': 'user_id'}, {'$inc': {'current_value': 1}}, return_document=True)['current_value']
            current_app.db.patients.insert_one({'user_id': user_id, 
                                                'email_id': email_id, 
                                                'password': password, 
                                                'first_name': first_name,
                                                'last_name': last_name, 
                                                'phone_number': phone_number, 
                                                'birthday': birthday, 
                                                'gender': gender})
            return redirect(url_for("auth.login"))
        else:
            existing_user = current_app.db.doctors.find_one({'$or': [{'email_id': email_id}, {'phone_number': phone_number}]})
            if existing_user is not None:
                return render_template('register.html', message="User already exists")
            user_id = current_app.db.meta.find_one_and_update({'field': 'user_id'}, {'$inc': {'current_value': 1}}, return_document=True)['current_value']
            current_app.db.doctors.insert_one({'user_id': user_id, 
                                               'email_id': email_id, 
                                               'password': password, 
                                               'first_name': first_name,
                                               'last_name': last_name, 
                                               'phone_number': phone_number, 
                                               'birthday': birthday, 
                                               'gender': gender})
            return redirect(url_for("auth.login"))
    return render_template('register.html', message="Create an account")


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email_id = request.form['email_id']
        password = request.form['password']

        user = current_app.db.patients.find_one({'email_id': email_id, 'password': password})
        if user is not None:
            session['user_id'] = user['user_id']
            session['role'] = 'patient'
            return redirect(url_for("patient.dashboard"))

        # if user is not found in patients collection, then check in doctors collection
        user = current_app.db.doctors.find_one({'email_id': email_id, 'password': password})
        if user is not None:
            session['user_id'] = user['user_id']
            session['role'] = 'doctor'
            return redirect(url_for("doctor.dashboard"))

        return render_template('login.html', message="Invalid email or password")

    return render_template('login.html', message="Login to your account")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))