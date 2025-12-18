from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checkout.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database model
class Checkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

# Create the database table
with app.app_context():
    db.create_all()

# Render the checkout page
@app.route('/checkout', methods=['GET'])
def checkout_page():
    return render_template('checkout.html')  # Ensure checkout.html is present in the templates folder

# Handle form submission
@app.route('/checkout', methods=['POST'])
def process_checkout():
    try:
        # Parse form data
        data = request.form
        name = data.get('name')
        email = data.get('email')
        address = data.get('address')
        mobile = data.get('mobile')
        total_amount = data.get('total_amount')

        # Validate data
        if not all([name, email, address, mobile, total_amount]):
            return jsonify({'error': 'All fields are required'}), 400

        # Save to database
        checkout_entry = Checkout(
            name=name,
            email=email,
            address=address,
            mobile=mobile,
            total_amount=float(total_amount)
        )
        db.session.add(checkout_entry)
        db.session.commit()

        return jsonify({'message': 'Checkout successful'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your checkout'}), 500

if __name__ == '__main__':
    app.run(debug=True)
