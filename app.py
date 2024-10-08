from flask import Flask
from create_quiz import create_quiz_bp, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app.
db.init_app(app)

# Register the blueprint with the app.
app.register_blueprint(create_quiz_bp)

# Create the tables when the app starts.
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
