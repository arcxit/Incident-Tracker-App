from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    severity = db.Column(db.String(20), default="Low")  # Low/Medium/High
    status = db.Column(db.String(20), default="Open")   # Open/In Progress/Resolved
    notes = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
