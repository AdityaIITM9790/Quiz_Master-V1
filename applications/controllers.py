from flask import Flask, render_template, request, session
from flask import current_app as app
from .models import *
from applications.database import db

# app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login page
    '''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user exists in database
        this_user = User.query.filter_by(
            email=email, password=password).first()

        if this_user:
            if this_user.password == password:
                if this_user.role == 'admin':  # Redirect admin to admin dashboard
                    all_subjects = Subject.query.all()
                    return render_template('admin_dash.html', this_user=this_user, subjects=all_subjects)
                else:  # Redirect normal users to user dashboard
                    return render_template('user_dash.html', this_user=this_user)

        return render_template('login.html', error="Invalid credentials, please try again.")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Register page'''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('name')
        qualification = request.form.get('qualification')
        dob = request.form.get('dob')

        # Check if the user already exists
        this_user = User.query.filter_by(email=email).first()
        if this_user: # will redirect to login page if user already exists
            return render_template('register.html')

        # Create new user if not exists
        new_user = User(
            username=username, email=email, password=password,
            full_name=full_name, qualification=qualification, dob=dob, role="user"
        )
        db.session.add(new_user)
        db.session.commit()

        return render_template('login.html')

    return render_template('register.html')


@app.route('/logout')
def logout():
    '''
    Logout page
    '''
    session.pop('user', None)
    session.pop('role', None)
    return render_template('login.html', message="You have been logged out.")


@app.route('/add_subject')
def add_subject():
    '''
    Adding a new subject
    '''
    return render_template('add_subject.html')


@app.route('/save_subject', methods=['POST'])
def save_subject():
    '''
    Saving the subject in the database
    '''
    subject_name = request.form.get('subject_name')
    subject_description = request.form.get('subject_description')
    

    # Save the subject in the database
    new_subject = Subject(name=subject_name, description=subject_description)
    db.session.add(new_subject)
    db.session.commit()

    admin_user = User.query.filter_by(role='admin').first()
    all_subjects = Subject.query.all()

    return render_template('admin_dash.html', this_user=admin_user, subjects = all_subjects)


@app.route('/add_chapter/<int:subject_id>')
def add_chapter(subject_id):
    '''
    Adding a new chapter based on the subject id
    '''
    return render_template('add_chapters.html', subject_id=subject_id)

@app.route('/save_chapter/<int:subject_id>', methods=['POST'])
def save_chapter(subject_id):
    chapter_name = request.form.get('chapter_name')
    description = request.form.get('description')
    num_questions = request.form.get('num_questions')

    # Create new chapter using subject_id from URL
    new_chapter = Chapter(name=chapter_name, description=description,
                          subject_id=subject_id, num_questions=num_questions)
    
    admin_user = User.query.filter_by(role='admin').first()
    subjects = Subject.query.all()  
    chapters = Chapter.query.all()

    db.session.add(new_chapter)
    db.session.commit()

    return render_template('admin_dash.html', this_user=admin_user, subjects=subjects, chapters=chapters)

@app.route('/edit_chapter/<int:chapter_id>')
def edit_chapter(chapter_id):
    '''
    Editing a chapter i.r. removing or increasing the quiz questions based on the chapter id
    '''
    chapter = Chapter.query.get(chapter_id)
    return render_template('edit_chapter.html', chapter=chapter)


@app.route('/delete_chapter/<int:chapter_id>')
def delete_chapter(chapter_id):
    '''
    Deleting a chapter based on the chapter id'''
    chapter = Chapter.query.get(chapter_id)
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
    admin_user = User.query.filter_by(role='admin').first()
    chapters = Chapter.query.all()

    return render_template('admin_dash.html', subjects=Subject.query.all(),this_user=admin_user,chapters=chapters)

@app.route('/admin_dash')
def admin_dashboard():
    '''
    Render the admin dashboard with subjects and chapters.
    '''
    admin_user = User.query.filter_by(role='admin').first()
    subjects = Subject.query.all()
    
    return render_template('admin_dash.html', this_user=admin_user, subjects=subjects)

################################# QUIZ Sesion ############################################
@app.route('/quiz_creator')
def quiz_creator():
    '''
    Display Quiz Creator Tool page
    '''

    admin_user = User.query.filter_by(role='admin').first()
    subjects = Subject.query.all()
    return render_template('quiz_creator.html',this_user=admin_user, subjects=subjects)


@app.route('/add_quiz/<int:subject_id>')
def add_quiz(subject_id):
    '''
    Render quiz creation page for a specific subject.
    '''
    subject = Subject.query.get(subject_id)
    return render_template('add_quiz.html', subject=subject)

