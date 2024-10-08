from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

##########################################
####
####
####        Caton Changes
####
####
###########################################


#Creating the initial trivia quizzes for the website.
# Quizzes is a dictionary where we will be storing our trivia questions
# Each trivia will have a unique id key, which is basically just an increasing increment of the amount of trivia we have right now
# It is stored in the quiz_id variable
quizzes = [
    {
        "id": 1,
        "title": "General Knowledge",
        "description": "A quiz to test your general knowledge.",
        "trivia": [
            {
                "question": "What is the capital of France?",
                "options": ["Paris", "London", "Rome", "Berlin"],
                "correct_answer": "Paris"
            }
        ]
    },
    {
        "id": 2,
        "title": "Science Quiz",
        "description": "A quiz to test your knowledge of science.",
        "trivia": [
            {
                "question": "What is the chemical symbol for water?",
                "options": ["H2O", "CO2", "O2", "N2"],
                "correct_answer": "H2O"
            }
        ]
    }
]

# Variable to give ID to new trivias.
# Should only be called on create_quiz, and to be incremented by one.
# Has initial value of 2 as we have 2 pregenerated quizzes so far.
quiz_id = 2


##########################################
####
####
####        Caton Changes
####
####
###########################################

@app.route("/")
def home():
  return render_template('base.html')

@app.route("/create_quiz", methods=['GET', 'POST'])
def create_quiz():
    global quiz_id 

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        numQuestions = int(request.form['num_questions'])

        # Debugging: Printing initial data.
        print(f"Title: {title}, Description: {description}, Number of Questions: {numQuestions}")
        
        # Creating a temporary dictionary to append to the quizzes dictionary later
        temp_trivia = []

        for i in range(1, numQuestions + 1):
            question =  request.form[f'question{i}']
            options = request.form[f'answer{i}'].split(', ') #Splits the comma from the options
            correct_answer = request.form[f'correct{i}']


            # Debugging: Print each question's data
            print(f"Question {i}: {question}")
            print(f"Options: {options}")
            print(f"Correct Answer: {correct_answer}")

            # Converting the prompt into a temporary dictionary, and appending it to temp_trivia each time
            question_dict = {
                "question":  question,
                "options": options,
                "correct_answer": correct_answer
            }
            # Appending it to the temp_trivia
            temp_trivia.append(question_dict)

        # Finish creating a new quiz dictionary
        new_quiz = {
            "id": quiz_id + 1,
            "title": title,
            "description": description,
            "trivia": temp_trivia
        }

        # Append this new trivia to the quizzes dictionary
        quizzes.append(new_quiz)

        # Add one to the quiz_id as we just added a new quiz
        quiz_id += 1

        # Debugging: Print the entire quizzes list to verify the new quiz was added
        print(f"New Quiz Added: {new_quiz}")

        # redirecting back to the home page
        return redirect(url_for('home'))
    # Give the user the create quiz form
    return render_template('create_quiz.html')

if __name__ == "__main__":
  app.run()
