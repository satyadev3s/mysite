from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/messages")
def view_messages():
    messages = Contact.query.all()

    return jsonify([
        {
            "id": msg.id,
            "name": msg.name,
            "email": msg.email,
            "message": msg.message
        }
        for msg in messages
    ])
@app.route("/debug")
def debug():
    messages = Contact.query.all()
    for msg in messages:
        print(msg.name, msg.email, msg.message)
    return "Check terminal"
@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json(force=True)
        print("Received:", data)

        new_message = Contact(
            name=data.get("name"),
            email=data.get("email"),
            message=data.get("message")
        )

        db.session.add(new_message)
        db.session.commit()

        print("Saved Successfully")

        return jsonify({"message": "Message Sent Successfully 🚀"})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"message": str(e)}), 500
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)