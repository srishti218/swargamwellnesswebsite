from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///education_visits.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///education_visits.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class EducationVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    slot = db.Column(db.String(20), nullable=False)

# Create the database tables
# with app.app_context():
#     db.create_all()
with app.app_context():
    try:
        db.create_all()
        print("Database and tables created successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")
# Route to handle form submissions
@app.route('/education_visit', methods=['POST'])
def education_visit():
    try:
        # Parse JSON request data
        data = request.get_json()
        name = data.get('name')
        mobile = data.get('mobile')
        email = data.get('email')
        slot = data.get('slot')

        # Validate input
        if not all([name, mobile, email, slot]):
            return jsonify({'error': 'All fields are required'}), 400

        # Save to the database
        visit = EducationVisit(name=name, mobile=mobile, email=email, slot=slot)
        print(db.session.add(visit))
        db.session.commit()

        return jsonify({'message': 'Form submitted successfully'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
