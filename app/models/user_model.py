import json
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Worker(UserMixin, db.Model):
    __tablename__ = "trabajador"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    roles = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, password, roles=["user"]):
        self.name = name
        self.email= email
        self.password_hash = generate_password_hash(password)
        self.roles = json.dumps(roles)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_by_name(name):
        return Worker.query.filter_by(name=name).first()