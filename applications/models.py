from .database import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    full_name = db.Column(db.String(), nullable=False)
    qualification = db.Column(db.String(), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(), nullable=False, default='user')  # 'admin' or 'user'

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text, nullable=True)
    num_questions = db.Column(db.Integer, nullable=False, default=0)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete="CASCADE"), nullable=False)
    subject = db.relationship('Subject', backref=db.backref('chapters', lazy=True, cascade="all, delete"))

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    chapter = db.relationship('Chapter', backref='quizzes', lazy=True)  # <-- Added this line
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.String(5), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    num_questions = db.Column(db.Integer, nullable=False, default=0)

    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    title = db.Column(db.String(), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(), nullable=False)
    option_b = db.Column(db.String(), nullable=False)
    option_c = db.Column(db.String(), nullable=False)
    option_d = db.Column(db.String(), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # A, B, C, or D

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, nullable=False)
    total_scored = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('scores', lazy=True))
    quiz = db.relationship('Quiz', backref=db.backref('scores', lazy=True))
