from flask import Blueprint, request, jsonify
from app.models import db, User

users_blp = Blueprint('users', __name__)

@users_blp.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST': # POST요청이 들어오면, Json데이터에서 username과 email을 추출
        data = request.get_json() # 클라이언트에서 보낸 JSON 데이터를 받아옴
        username = data.get('username') # get() 메서드를 사용하여 'username' 추출
        email = data.get('email') # 'email' 추출

        # username 또는 email이 없으면 오류 메시지 반환
        if not username or not email:
            return jsonify({'msg':'Username and email are empty.'}), 400
    
        # 새로운 사용자 객체 생성
        new_user = User(username=username, email=email) 

        # 새로 생성한 사용자 객체를 세션에 추가
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'msg':'Successfully added user'}), 201 # 성공적으로 추가된 경우, 201 상태 코드 반환

    if request.method == "GET": # GET요청이 들어오면, 모든 사용자 목록을 반환
        users = User.query.all() # 모든 사용자 정보를 데이터베이스에서 조회
        user_list = [{'username':user.username, 'email':user.email} for user in users] # 각 사용자 정보를 리스트에 담음
        return jsonify(user_list), 200 # 사용자 목록을 JSON 형태로 반환, 200 상태 코드
    
@users_blp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    # username이나 email이 없으면 오류 메시지 반환
    if not username or not email:
        return jsonify({'msg':'Username and email are empty.'}), 400
    
    # 해당 사용자 ID로 사용자 조회
    user = User.query.get(user_id)
    if not user :
        return jsonify({'msg':'User not found.'}), 404 # 사용자가 없으면 404 Not Found 반환
    
    # 사용자 정보 수정
    user.username = username
    user.email = email

    db.session.commit()

    return jsonify({'msg':'Successfully user update.'}), 200
    
@users_blp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg':'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg':'Successfully delete user'}), 200
    
