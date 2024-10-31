from flask import Flask, redirect, render_template, request, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from user import User
from create_quiz import create_quiz_bp, Quiz, Question

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'cmpt_276_trivia'

# Initialize the database with the app
db.init_app(app)

# Register the blueprint with the app
app.register_blueprint(create_quiz_bp)

@app.route("/")
def home():
    return render_template('base.html')

@app.route("/quizzes")
def quizzes():
    quizzes = Quiz.query.all()
    return render_template('quizzes.html', quizzes=quizzes)

@app.route("/play_quiz/<int:quiz_id>")
def play_quiz(quiz_id):
    # Reset score at the beginning of each quiz
    if "user_score" not in session:
        session["user_score"] = 0

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash("Quiz not found.")
        return redirect(url_for('quizzes'))

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    question_index = int(request.args.get('question_index', 0))

    if question_index < len(questions):
        current_question = questions[question_index]
    else:
        return redirect(url_for('final_score', quiz_id=quiz_id))  # Redirect to final score page

    quiz_data = {
        'quiz_id': quiz.id,
        'title': quiz.title,
        'description': quiz.description,
        'time_limit': quiz.time_limit,
        'current_question': {
            'question_text': current_question.question_text,
            'options': {
                '1': current_question.option1,
                '2': current_question.option2,
                '3': current_question.option3,
                '4': current_question.option4
            },
            'correct_answer': current_question.correct_answer
        }
    }

    return render_template("play_quiz.html", quiz=quiz_data, current_question=question_index)

@app.route("/update_score", methods=["POST"])
def update_score():
    data = request.get_json()
    increment = data.get("increment", 0)

    # Accumulate the score in session
    session["user_score"] = session.get("user_score", 0) + increment
    return jsonify({"user_score": session["user_score"]})

@app.route("/final_score/<int:quiz_id>")
def final_score(quiz_id):
    total_questions = Question.query.filter_by(quiz_id=quiz_id).count()
    user_score = session.get("user_score", 0)
    session.pop("user_score", None)  # Clear the score after displaying it
    return render_template("final_score.html", user_score=user_score, total_questions=total_questions)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Login successful")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("signup"))
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose another one.")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        flash("Account created successfully! You are now logged in.")
        return redirect(url_for("home"))

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_score", None)  # Clear the score on logout
    flash("Successfully logged out.")
    return redirect(url_for("home"))

@app.route('/show_questions', methods=['GET'])
def show_questions():
    questions = Question.query.all()
    questions_data = [
        {
            "id": question.id,
            "quiz_id": question.quiz_id,
            "question_text": question.question_text,
            "option1": question.option1,
            "option2": question.option2,
            "option3": question.option3,
            "option4": question.option4,
            "correct_answer": question.correct_answer
        }
        for question in questions
    ]
    return jsonify(questions_data)

if __name__ == "__main__":
    app.run(debug=True)
