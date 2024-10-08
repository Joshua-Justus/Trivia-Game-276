from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
  return render_template('base.html')

@app.route("/create_quiz")
def create_quiz():
    return render_template('create_quiz.html')
  
@app.route("/quizzes")
def quiz():
    return render_template('quizzes.html')

if __name__ == "__main__":
  app.run()
