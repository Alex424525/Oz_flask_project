from flask import Blueprint, request, jsonify, render_template
from app.models import db, User

users_blp = Blueprint('users', __name__)

@users_blp.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':  # 사용자 추가
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        email = data.get('email')

        if not name or not age or not gender or not email:
            return jsonify({'msg': 'Name, age, gender, and email are required.'}), 400

        new_user = User(name=name, age=age, gender=gender, email=email)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'msg': f'{name}님 회원가입을 축하합니다!', 'user_id': new_user.id}), 201

    if request.method == 'GET':  # 모든 사용자 조회
        users = User.query.all()
        user_list = [user.to_dict() for user in users]  # JSON 직렬화 가능하도록 변경
        return jsonify(user_list), 200

@users_blp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """특정 유저를 ID로 조회"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    return jsonify(user.to_dict()), 200

@users_blp.route('/users/email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    """특정 유저를 이메일로 조회"""
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    return jsonify(user.to_dict()), 200

#<--html-->
@users_blp.route("/", methods = ['GET'])
def home():
    return render_template("register.html")