from flask import Flask, render_template, request, session
from flask import current_app as app
from .models import *
from applications.database import db

# app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user exists in database
        this_user = User.query.filter_by(
            email=email, password=password).first()

        if this_user:
            if this_user.password == password:
                if this_user.role == 'admin':  # Redirect admin to admin dashboard
                    return render_template('admin_dash.html', this_user=this_user)
                else:  # Redirect normal users to user dashboard
                    return render_template('user_dash.html', this_user=this_user)

        return render_template('login.html', error="Invalid credentials, please try again.")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('name')
        qualification = request.form.get('qualification')
        dob = request.form.get('dob')

        # Check if the user already exists
        this_user = User.query.filter_by(email=email).first()
        if this_user:
            return render_template('register.html', error="User already exists. Please log in.")

        # Create new user if not exists
        new_user = User(
            username=username, email=email, password=password,
            full_name=full_name, qualification=qualification, dob=dob, role="user"
        )
        db.session.add(new_user)
        db.session.commit()

        return render_template('login.html', message="Registration successful. Please log in.")

    return render_template('register.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' in session and session.get('role') == 'admin':
        return render_template('admin_dashboard.html', user=session['user'])
    return render_template('login.html', error="Please log in first.")


@app.route('/user_dashboard')
def user_dashboard():
    if 'user' in session and session.get('role') == 'user':
        return render_template('user_dashboard.html', user=session['user'])
    return render_template('login.html', error="Please log in first.")


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return render_template('login.html', message="You have been logged out.")
