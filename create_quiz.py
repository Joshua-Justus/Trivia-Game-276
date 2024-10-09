from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from user import User

# Create a Blueprint for quiz-related routes.
create_quiz_bp = Blueprint('create_quiz_bp', __name__)

# Define the Quiz model to store basic quiz information.
class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)  # Time limit in minutes

# Define the Question model to store questions for each quiz.
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.String(255), nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)

# Define the route to render the base (home) page.
@create_quiz_bp.route('/')
def home():
    return render_template('base.html')

# Define the route to render the create quiz page.
@create_quiz_bp.route('/create_quiz', methods=['GET'])
def create_quiz_page():
    return render_template('create_quiz.html')

# Define the route to handle quiz creation.
@create_quiz_bp.route('/create_quiz', methods=['POST'])
def create_quiz():
    # Check if the user is logged in
    if "user_id" not in session:
        flash("You must be logged in to create a quiz.")
        # Redirects them to the login page
        return redirect(url_for("login"))
        
    # Retrieve the data from the form.
    title = request.form.get('title')
    description = request.form.get('description')
    time_limit = request.form.get('time_limit')
    num_questions = int(request.form.get('num_questions'))

    # Create a new Quiz object and add it to the database.
    new_quiz = Quiz(title=title, description=description, time_limit=int(time_limit))
    db.session.add(new_quiz)
    db.session.commit()

    # Save each question for the quiz.
    for i in range(1, num_questions + 1):
        question_text = request.form.get(f'question{i}')
        option1 = request.form.get(f'answer{i}1')
        option2 = request.form.get(f'answer{i}2')
        option3 = request.form.get(f'answer{i}3')
        option4 = request.form.get(f'answer{i}4')
        correct_answer = request.form.get(f'correct{i}')

        # Create a new Question object for each question.
        new_question = Question(
            quiz_id=new_quiz.id,
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer=correct_answer
        )
        db.session.add(new_question)

    # Commit all changes to the database.
    db.session.commit()

    # Redirect back to the home page or show a success message.
    return redirect(url_for('create_quiz_bp.home'))
