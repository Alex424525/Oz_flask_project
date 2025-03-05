# app/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo
from enum import Enum
from flask import abort

db = SQLAlchemy()  # 여기서 db 객체를 생성
KST = ZoneInfo("Asia/Seoul")

class CommonModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(tz=KST), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(tz=KST),
        onupdate=lambda: datetime.now(tz=KST),
        nullable=False,
    )

# User 모델: 문자열 기반으로 하고 CheckConstraint를 사용하여 검증
class User(CommonModel):
    __tablename__ = "users"
    name = db.Column(db.String(10), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    __table_args__ = (
        db.CheckConstraint("age IN ('teen', 'twenty', 'thirty', 'fourty', 'fifty')", name="check_age"),
        db.CheckConstraint("gender IN ('male', 'female')", name="check_gender"),
    )

    def __init__(self, name, age, gender, email):
        allowed_ages = {"teen", "twenty", "thirty", "fourty", "fifty"}
        allowed_genders = {"male", "female"}

        if User.query.filter_by(email=email).first():
            abort(400, "이미 존재하는 계정 입니다.")

        if age not in allowed_ages:
            abort(400, f"Invalid age: {age}. Allowed values: {allowed_ages}")

        if gender not in allowed_genders:
            abort(400, f"Invalid gender: {gender}. Allowed values: {allowed_genders}")

        self.name = name
        self.age = age
        self.gender = gender
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

# Image 모델: 문자열 타입을 사용하고 CheckConstraint로 검증하며 __init__에서 타입을 검증
class Image(CommonModel):
    __tablename__ = "images"
    url = db.Column(db.TEXT, nullable=False)
    type = db.Column(db.String(10), nullable=False)

    __table_args__ = (
        db.CheckConstraint("type IN ('main', 'sub')", name="check_image_type"),
    )

    def __init__(self, url, image_type):
        allowed_types = {"main", "sub"}
        if image_type not in allowed_types:
            abort(400, f"Invalid type: {image_type}. Allowed values: {allowed_types}")
        self.url = url
        self.type = image_type

    questions = db.relationship("Question", back_populates="image")

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "type": self.type,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

# Question 모델
class Question(CommonModel):
    __tablename__ = "questions"
    title = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    sqe = db.Column(db.Integer, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=False)

    image = db.relationship("Image", back_populates="questions")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "is_active": self.is_active,
            "sqe": self.sqe,
            "image": self.image.to_dict() if self.image else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

# Choices 모델
class Choices(CommonModel):
    __tablename__ = "choices"
    content = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    sqe = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "is_active": self.is_active,
            "sqe": self.sqe,
            "question_id": self.question_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

# Answer 모델
class Answer(CommonModel):
    __tablename__ = "answers"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    choice_id = db.Column(db.Integer, db.ForeignKey("choices.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "choice_id": self.choice_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
