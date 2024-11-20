from app import db
from datetime import datetime

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    source = db.Column(db.String(100))
    theme = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    url = db.Column(db.String(500))
    image_url = db.Column(db.String(500))  # Ajout du champ pour l'image