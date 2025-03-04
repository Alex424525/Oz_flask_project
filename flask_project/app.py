from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Question('{self.title}')"


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String(200), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    question = db.relationship('Question', backref=db.backref('choices', lazy=True))

    def __repr__(self):
        return f"Choice('{self.choice_text}')"


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Image('{self.url}')"


# CRUD 함수들
def create_user(username, email):
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()


def get_user(user_id):
    return User.query.get(user_id)


def create_question(title):
    new_question = Question(title=title)
    db.session.add(new_question)
    db.session.commit()


def get_question(question_id):
    return Question.query.get(question_id)


def create_choice(choice_text, question_id):
    question = Question.query.get(question_id)
    if not question:
        return None
    new_choice = Choice(choice_text=choice_text, question_id=question.id)
    db.session.add(new_choice)
    db.session.commit()


def get_choices_for_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return None
    return question.choices


def create_image(url):
    new_image = Image(url=url)
    db.session.add(new_image)
    db.session.commit()


def get_image(image_id):
    return Image.query.get(image_id)


# Flask 라우트 설정
@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    create_user(data['username'], data['email'])
    return jsonify({'message': 'User created successfully'}), 201


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    user = get_user(user_id)
    if user:
        return jsonify({'username': user.username, 'email': user.email})
    return jsonify({'message': 'User not found'}), 404


@app.route('/question', methods=['POST'])
def add_question():
    data = request.get_json()
    create_question(data['title'])
    return jsonify({'message': 'Question created successfully'}), 201


@app.route('/question/<int:question_id>', methods=['GET'])
def get_question_data(question_id):
    question = get_question(question_id)
    if question:
        return jsonify({'title': question.title})
    return jsonify({'message': 'Question not found'}), 404


@app.route('/choice', methods=['POST'])
def add_choice():
    data = request.get_json()
    create_choice(data['choice_text'], data['question_id'])
    return jsonify({'message': 'Choice created successfully'}), 201


@app.route('/choices/<int:question_id>', methods=['GET'])
def get_choices(question_id):
    choices = get_choices_for_question(question_id)
    if choices:
        return jsonify([{'choice_text': choice.choice_text} for choice in choices])
    return jsonify({'message': 'Choices not found for this question'}), 404


@app.route('/image', methods=['POST'])
def add_image():
    data = request.get_json()
    create_image(data['url'])
    return jsonify({'message': 'Image created successfully'}), 201


@app.route('/image/<int:image_id>', methods=['GET'])
def get_image_data(image_id):
    image = get_image(image_id)
    if image:
        return jsonify({'url': image.url})
    return jsonify({'message': 'Image not found'}), 404


if __name__ == "__main__":
    app.run(debug=True)

