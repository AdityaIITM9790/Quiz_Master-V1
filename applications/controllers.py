from flask import Flask, render_template, request, session, redirect
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
                    quizzes = Quiz.query.all()  # Fetch all quizzes
                    return render_template('user_dash.html', quizzes=quizzes, this_user=this_user)

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
        if this_user:  # will redirect to login page if user already exists
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

    return render_template('admin_dash.html', this_user=admin_user, subjects=all_subjects)


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

    return render_template('admin_dash.html', subjects=Subject.query.all(), this_user=admin_user, chapters=chapters)


@app.route('/admin_dash')
def admin_dashboard():
    '''
    Render the admin dashboard with subjects and chapters.
    '''
    admin_user = User.query.filter_by(role='admin').first()
    subjects = Subject.query.all()

    return render_template('admin_dash.html', this_user=admin_user, subjects=subjects)


################################# USER Dashboard ############################################

@app.route('/user_dash')
def user_dash():
    """
    Display the user dashboard with all available quizzes.
    """
    quizzes = Quiz.query.all()  # Fetch all quizzes
    user = User.query.filter_by(role='user').first()  # Get the logged-in user
    # chapters = Chapter.query.all()  # Fetch chapters

     # Ensure quizzes load related questions
    for quiz in quizzes:
        quiz.num_questions = len(quiz.questions)  # Force load questions


    return render_template('user_dash.html', quizzes=quizzes, this_user=user)


@app.route('/start_quiz/<int:quiz_id>')
def start_quiz(quiz_id):
    """
    Start the quiz.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('start_quiz.html', quiz=quiz)



################################# QUIZ Sesion ############################################


@app.route('/quiz_creator', methods=['GET'])
def quiz_creator():
    '''
    Display Quiz Creator Tool page
    '''
    admin_user = User.query.filter_by(role='admin').first()
    search_query = request.args.get('chap_name', '')

    if not admin_user or admin_user.role != 'admin':
        return render_template('login.html', error="Unauthorized access!")
    
    if search_query:
        quizzes = Quiz.query.join(Chapter).filter(Chapter.name.ilike(f"%{search_query}%")).all()
    else:
        quizzes = Quiz.query.all()


    return render_template('quiz_creator.html', quizzes=quizzes, this_user=admin_user)


# Route to add a new quiz
@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        chapter_id = request.form.get('chapter_id')
        date_of_quiz = request.form.get('date_of_quiz')
        time_duration = request.form.get('time_duration')
        remarks = request.form.get('remarks')
        num_questions = request.form.get("num_questions")

        if chapter_id:
            new_quiz = Quiz(chapter_id=chapter_id, date_of_quiz=date_of_quiz, time_duration=time_duration, remarks=remarks,num_questions=int(num_questions))
            db.session.add(new_quiz)
            db.session.commit()

    chapters = Chapter.query.all()
    return render_template('add_quiz.html', chapters=chapters)

# Route to save quiz in the database


@app.route('/save_quiz', methods=['POST'])
def save_quiz():
    # Get chapter_id directly from form
    chapter_id = request.form.get('chapter_id')
    date_of_quiz = request.form.get('date_of_quiz')
    time_duration = request.form.get('time_duration')
    remarks = request.form.get('remarks')

    if chapter_id:
        new_quiz = Quiz(
            chapter_id=chapter_id,
            date_of_quiz=date_of_quiz,
            time_duration=time_duration,
            remarks=remarks
        )
        db.session.add(new_quiz)
        db.session.commit()

    quizzes = Quiz.query.all()
    
    return render_template('quiz_creator.html', quizzes=quizzes, this_user=User.query.filter_by(role='admin').first())


@app.route('/delete_quiz/<int:quiz_id>')
def delete_quiz_route(quiz_id):
    '''
    Delete a quiz based on the quiz id
    '''
    quiz = Quiz.query.get(quiz_id)
    if quiz:
        db.session.delete(quiz)
        db.session.commit()

    quizzes = Quiz.query.all()
    return render_template('quiz_creator.html', quizzes=quizzes, this_user=User.query.filter_by(role='admin').first())

@app.route('/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    
    if request.method == 'POST':
        if quiz:
            quiz.date_of_quiz = request.form.get('date_of_quiz')
            quiz.time_duration = request.form.get('time_duration')
            quiz.remarks = request.form.get('remarks')
            quiz.num_questions = int(request.form.get('num_questions', 0))  

            db.session.commit()  # Save the changes
        quizzes = Quiz.query.all()
        return render_template('quiz_creator.html', quizzes=quizzes, this_user=User.query.filter_by(role='admin').first())

    return render_template('edit_quiz.html', quiz=quiz)  # Show the edit form

@app.route('/add_question/<int:chapter_id>/<int:quiz_id>')
def add_question(chapter_id, quiz_id):
    quiz = Quiz.query.get(quiz_id)
    chapter = Chapter.query.get(chapter_id)

    if not quiz or not chapter:
        return "Invalid Quiz or Chapter", 404  # Handle invalid cases

    return render_template('add_question.html', chapter=chapter, quiz=quiz)


@app.route('/save_question/<int:quiz_id>', methods=['POST'])
def save_question(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    chapter = Chapter.query.get(quiz.chapter_id)  # Ensure chapter is retrieved

    # Get form data
    title = request.form.get('question_title')
    statement = request.form.get('question_statement')
    option_a = request.form.get('option_a')
    option_b = request.form.get('option_b')
    option_c = request.form.get('option_c')
    option_d = request.form.get('option_d')
    correct_option = request.form.get('correct_option')

    # Save question
    new_question = Question(
        quiz_id=quiz.id,
        chapter_id=quiz.chapter_id,  
        title=title,
        question_statement=statement,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_option=correct_option
    )
    db.session.add(new_question)
    db.session.commit()

    quiz.num_questions = Question.query.filter_by(quiz_id=quiz.id).count()
    db.session.commit()
    # Reload add_question.html with the chapter name
    quizzes = Quiz.query.all()
    return render_template('quiz_creator.html', quizzes=quizzes, this_user=User.query.filter_by(role='admin').first())
