#I've just added some boilerplate code to check if the redirects are working properly

from flask import Blueprint, render_template, url_for, current_app, session

doctor_bp = Blueprint('doctor', __name__ , url_prefix='/doctor')

@doctor_bp.route('/dashboard')
def dashboard():
    doctor_data = current_app.db.doctors.find_one({'user_id': session['user_id']})
    print(session['user_id'])

    if doctor_data is None:
        return "No doctor found", 404

    #Define the paths to your images
    image_paths = [url_for('static', filename='images/case-1.jpg'),
                   url_for('static', filename='images/case-2.png')]
    return render_template('doctor_dash.html', doctor=doctor_data, image_paths=image_paths)