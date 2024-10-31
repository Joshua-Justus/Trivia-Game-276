from flask import Flask, redirect, render_template, request, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from user import User
from create_quiz import create_quiz_bp, Quiz, Question

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'cmpt_276_trivia'

# Initialize the database with the app.
db.init_app(app)

# Register the blueprint with the app.
app.register_blueprint(create_quiz_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template('base.html')

# Route to display all available quizzes
@app.route("/quizzes")
def quizzes():
    # Retrieve all quizzes from the database
    quizzes = Quiz.query.all()
    return render_template('quizzes.html', quizzes=quizzes)

# Route to display a specific quiz by ID, including its questions
@app.route("/play_quiz/<int:quiz_id>")
def play_quiz(quiz_id):
    # Retrieve the quiz by ID
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash("Quiz not found.")
        return redirect(url_for('quizzes'))

    # Retrieve all questions for the selected quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    # Set the initial question index (if no question index is specified in the URL)
    question_index = int(request.args.get('question_index', 0))

    # Check if the question index is within the bounds of the question list
    if question_index < len(questions):
        current_question = questions[question_index]
    else:
        # Redirect to quiz list if all questions are answered
        return redirect(url_for('final_score', quiz_id=quiz_id))  # New code to redirect to final_score.html

    # Format the quiz data for display
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

@app.route("/final_score/<int:quiz_id>")
def final_score(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    total_questions = quiz.total_questions
    user_score = 0 # session.get('user_score', 0)  

    return render_template("final_score.html", user_score=user_score, total_questions=total_questions)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Try to find the user by username
        user = User.query.filter_by(username=username).first()

        # Check if user exists and the password is correct
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

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("signup"))
        
        # Check for existing usernames
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose another one.")
            return redirect(url_for("signup"))

        # Register the new user with hashed password
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Log the user in automatically after successful signup
        session["user_id"] = new_user.id
        flash("Account created successfully! You are now logged in.")
        return redirect(url_for("home"))

    return render_template("signup.html")


@app.route("/logout")
def logout():
    # Clears the session data.
    session.pop("user_id", None)  
    flash("Successfully logged out.")
    return redirect(url_for("home"))


# Show questions from the database as JSON for API access (optional)
@app.route('/show_questions', methods=['GET'])
def show_questions():
    questions = Question.query.all()
    
    # Format the result as a list of dictionaries
    questions_data = []
    for question in questions:
        questions_data.append({
            "id": question.id,
            "quiz_id": question.quiz_id,
            "question_text": question.question_text,
            "option1": question.option1,
            "option2": question.option2,
            "option3": question.option3,
            "option4": question.option4,
            "correct_answer": question.correct_answer
        })
    
    # Return the data as JSON
    return jsonify(questions_data)


if __name__ == "__main__":
    app.run(debug=True)
