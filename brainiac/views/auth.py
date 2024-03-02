from flask import Blueprint, redirect, render_template, request, session, url_for

auth_bp = Blueprint('auth', __name__ )

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        joke = request.form['joke']
        return redirect(url_for("auth.login"))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for("patient.dashboard"))
    
    return render_template('login.html')