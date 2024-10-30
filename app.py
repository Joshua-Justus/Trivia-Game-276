from flask import Flask, redirect, render_template, request, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash  # Import for password security
from models import db
from user import User
from create_quiz import create_quiz_bp, Quiz, Question

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/rushilsehgal/Library/CloudStorage/OneDrive-SimonFraserUniversity(1sfu)/Trivia-website/quiz.db'  # Database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set a secret key for Flask. Helps for the flash, the updating messages.
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

@app.route("/quizzes")
def quiz():
    return render_template('quizzes.html')

# Sample quiz data for testing
sample_quiz = {
    'id': 1,
    'title': 'General Knowledge Quiz',
    'questions': [
        {'text': 'What is the capital of France?', 'answers': ['Paris', 'London', 'Rome', 'Berlin'], 'correct': 'Paris'},
        {'text': 'What is 2 + 2?', 'answers': ['3', '4', '5', '6'], 'correct': '4'},
        {'text': 'What is the largest ocean on Earth?', 'answers': ['Indian Ocean', 'Atlantic Ocean', 'Arctic Ocean', 'Pacific Ocean'], 'correct': 'Pacific Ocean'},
    ]
}

# Made Changes Here
@app.route("/play_quiz/<int:quiz_id>")
def play_quiz(quiz_id):
    # Retrieve the ID from the database:
    quiz = Quiz.query.get(quiz_id)
    # Redirect if the Quiz does not exist
    if not quiz:
        return redirect(url_for("quiz"))

    # Get the questions from the Database
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    print("Questions Retrieved:", questions)
    # Redirect if the Questions are not found
    if not questions:
        return redirect(url_for("quiz"))
    
    # Parse the question index from the url
    question_index = request.args.get('question_index', default=0, type=int)

    # Returns the user back to the quizzes page if the question index exceeds the number of questions in the quiz
    if question_index >= len(questions):
        return redirect(url_for("quiz"))
    
    # Formatting of the quiz database for the front end
    current_question = questions[question_index]

    # Helps the formatting to match up with what we discussed
    padded_question_number = str(question_index + 1).zfill(2)

    correct_answer = current_question.correct_answer
    correct_answer_id = f"{quiz_id}.{padded_question_number}{correct_answer}"

    quiz_data = {
        "quiz_id": quiz.id,
        f"{quiz_id}.000": quiz.title,
        f"{quiz_id}.001": quiz.description,
        f"{quiz_id}.002": quiz.time_limit,
        f"{quiz_id}.{padded_question_number}0": current_question.question_text,
        "options": {
        f"{quiz_id}.{padded_question_number}1": current_question.option1,
        f"{quiz_id}.{padded_question_number}2": current_question.option2,
        f"{quiz_id}.{padded_question_number}3": current_question.option3,
        f"{quiz_id}.{padded_question_number}4": current_question.option4,
        },
        "correct_answer": correct_answer_id
    }

    return render_template("play_quiz.html", quiz=quiz_data, current_question=question_index)

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


# Show questions from the database
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
