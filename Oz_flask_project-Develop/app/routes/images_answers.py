from flask import Blueprint, jsonify, request, Response , render_template
from app.models import db  # 이미 models.py에서 생성된 db 객체 사용

images_bp = Blueprint("images_answers", __name__)

# 앱의 모든 요청 전에 한 번 실행 (매 요청마다 실행되지는 않음)
@images_bp.before_app_request
def initialize_images():
    # 필요한 초기화 코드를 작성합니다.
    print("이미지 관련 초기화 작업 수행")

@images_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API 서버 연결 성공!"})

@images_bp.route('/image/main', methods=['GET'])
def get_main_image():
    return jsonify({"image_url": "https://example.com/main-image.jpg"})

@images_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    return jsonify({"message": f"회원가입이 완료되었습니다. {username}, {email}"}), 201

@images_bp.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    from app.models import Question  # 필요 시 models에서 가져오기
    question = Question.query.get_or_404(question_id)
    return jsonify({
        "question_id": question.id,
        "question_text": question.text,
        "choices": [choice.text for choice in question.choices]
    })

@images_bp.route('/questions/count', methods=['GET'])
def get_questions_count():
    from app.models import Question
    count = Question.query.count()
    return jsonify({"total_questions": count})

@images_bp.route('/choice/<int:question_id>', methods=['GET'])
def get_choices_route(question_id):
    from app.models import Question
    question = Question.query.get_or_404(question_id)
    choices = [choice.text for choice in question.choices]
    return jsonify({"question_id": question.id, "choices": choices})

@images_bp.route('/submit', methods=['POST'])
def submit_answer():
    from app.models import Answer
    data = request.get_json()
    question_id = data.get('question_id')
    answer_text = data.get('answer_text')
    answer = Answer(answer_text=answer_text, question_id=question_id)
    db.session.add(answer)
    db.session.commit()
    return jsonify({"message": "답변이 제출되었습니다!"}), 201

@images_bp.route('/image', methods=['POST'])
def create_image():
    data = request.get_json()
    image_url = data.get('image_url')
    return jsonify({"message": "이미지가 추가되었습니다.", "image_url": image_url}), 201

@images_bp.route('/question', methods=['POST'])
def create_question():
    from app.models import Question
    data = request.get_json()
    question_text = data.get('question_text')
    new_question = Question(text=question_text)
    db.session.add(new_question)
    db.session.commit()
    return jsonify({"message": "질문이 추가되었습니다!", "question_id": new_question.id}), 201

@images_bp.route('/choice', methods=['POST'])
def create_choice():
    from app.models import Choice, Question
    data = request.get_json()
    question_id = data.get('question_id')
    choice_text = data.get('choice_text')
    question = Question.query.get_or_404(question_id)
    new_choice = Choice(text=choice_text, question_id=question.id)
    db.session.add(new_choice)
    db.session.commit()
    return jsonify({"message": "선택지가 추가되었습니다!", "choice_text": new_choice.text}), 201


#<__html__>
@images_bp.route('/upload')
def upload_page():
    return render_template("image.html")
