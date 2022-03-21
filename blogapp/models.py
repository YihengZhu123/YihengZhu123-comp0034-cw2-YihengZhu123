from blogapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Blog(db.Model):
    __tablename__ = "blog"
    title = db.Column(db.Text, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    # timestamp = db.Column(db.)

class BlogComment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.email} {self.password}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
