from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=T
                   rue)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
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
            "phone": msg.phone,   # 🔥 ADD THIS
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
            phone=data.get("phone"),
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

with app.app_context():
    db.session.execute(text("DROP TABLE IF EXISTS contact"))
    db.session.execute(text("""
        CREATE TABLE contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            message TEXT
        )
    """))
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)

