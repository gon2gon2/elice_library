from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name