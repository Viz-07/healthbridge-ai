from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer,nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float,nullable=False)
    weight = db.Column(db.Float,nullable=False)
    blood_type = db.Column(db.String(5), nullable=False)
    allergies = db.Column(db.Text,nullable=True)
    past_illnesses = db.Column(db.Text,nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, name, email, password, age, gender, height, weight, blood_type, allergies=None, past_illnesses=None):
        self.name = name
        self.email = email
        self.set_password(password)
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.blood_type = blood_type
        self.allergies = allergies
        self.past_illnesses = past_illnesses

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender = db.Column(db.String(10), nullable=False) # 'user' or 'bot'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("Users", backref="chat_history")
