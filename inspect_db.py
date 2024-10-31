from create_quiz import db, Quiz, Question

# Create a Flask app context
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'  # Database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Query all quizzes
    quizzes = Quiz.query.all()
    print("\nQuizzes:")
    for quiz in quizzes:
        print(f"ID: {quiz.id}, Title: {quiz.title}, Description: {quiz.description}, Time Limit: {quiz.time_limit} minutes")

    # Query all questions
    questions = Question.query.all()
    print("\nQuestions:")
    for question in questions:
        print(f"user: {question.id}, Quiz ID: {question.quiz_id}, Question: {question.question_text}, Correct Answer: {question.correct_answer}")
