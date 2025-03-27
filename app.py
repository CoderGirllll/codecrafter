from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")  # Specify templates folder
CORS(app)

# SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///culture.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define Database Model
class CulturalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # "temple", "festival", "ritual"
    state = db.Column(db.String(100))
    religion = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    mythological_story = db.Column(db.Text)
    cultural_relevance = db.Column(db.Text)
    date = db.Column(db.String(20))  # For festivals

# Create the database
with app.app_context():
    db.create_all()

# Serve the custom HTML file as the homepage
@app.route("/")
def home():
    return render_template("index.html")  # Serves your index.html

# Add a new cultural entry
@app.route("/add", methods=["POST"])
def add_entry():
    data = request.json
    entry = CulturalEntry(**data)
    db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Entry added successfully!"}), 201

# Get all entries
@app.route("/entries", methods=["GET"])
def get_entries():
    entries = CulturalEntry.query.all()
    return jsonify([
        {
            "id": e.id, "name": e.name, "type": e.type, "state": e.state,
            "religion": e.religion, "description": e.description,
            "mythological_story": e.mythological_story, 
            "cultural_relevance": e.cultural_relevance, "date": e.date
        }
        for e in entries
    ])

if __name__ == "__main__":
    app.run(debug=True)
