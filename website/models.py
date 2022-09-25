from typing_extensions import Required
from wsgiref.validate import validator
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField
from wtforms.validators import DataRequired

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Rented(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column()

class UserForm(FlaskForm):
    full_name = StringField("fullname", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    age = StringField("age", validators=[DataRequired()])
    user_name = StringField("user_name", validators=[DataRequired()])
    submit = SubmitField("submit")
    


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.relationship('Note')

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100))
    name = db.Column(db.String(100))
    color = db.Column(db.String(100))
    location = db.Column(db.String(100))
    price = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

class PostForm(FlaskForm):
    brand = StringField("Brand", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    color = StringField("Color", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    submit = SubmitField()