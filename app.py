from flask import Flask, redirect, render_template, request, url_for

from create_quiz import (  # Import the blueprint and the database instance
    create_quiz_bp, db)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'  # Database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app.
db.init_app(app)

# Register the blueprint with the app.
app.register_blueprint(create_quiz_bp)

# Create the tables when the app starts.
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template('base.html')

@app.route("/quizzes")
def quiz():
    return render_template('quizzes.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle login logic here
        username = request.form['username']
        password = request.form['password']
        # Validate credentials, login user, etc.
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Handle sign up logic here
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Validate and create account logic
        return redirect(url_for("home"))
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
