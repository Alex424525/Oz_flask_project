from app.models import db, User

def create_user(name, age, gender, email):
    """새로운 사용자 추가"""
    if not name or not age or not gender or not email:
        return {'msg': 'Name, age, gender, and email are required.'}, 400

    new_user = User(name=name, age=age, gender=gender, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return {'msg': 'Successfully added user'}, 201

def get_all_users():
    """모든 사용자 조회"""
    users = User.query.all()
    return [
        {'id': user.id, 'name': user.name, 'age': user.age, 'gender': user.gender, 'email': user.email}
        for user in users
    ], 200

def get_user_by_id(user_id):
    """user_id로 특정 사용자 조회"""
    user = User.query.get(user_id)
    if not user:
        return {'msg': 'User not found'}, 404
    
    return {
        'id': user.id,
        'name': user.name,
        'age': user.age,
        'gender': user.gender,
        'email': user.email
    }, 200

def get_user_by_email(email):
    """email로 특정 사용자 조회"""
    user = User.query.filter_by(email=email).first()
    if not user:
        return {'msg': 'User not found'}, 404
    
    return {
        'id': user.id,
        'name': user.name,
        'age': user.age,
        'gender': user.gender,
        'email': user.email
    }, 200