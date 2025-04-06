# models.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # Stockez le hash du mot de passe, pas le mot de passe lui-même!
    audios = db.relationship('Audio', backref='author', lazy=True) #relation one to many

    def __repr__(self):
        return f"User('{self.email}')"

class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False) # Nom du fichier sur S3
    transcription = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #clé etrangere

    def __repr__(self):
        return f"Audio('{self.filename}')"