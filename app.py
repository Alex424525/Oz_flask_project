from flask import Flask, jsonify, request

app = Flask(__name__)

# 1. 기본 연결 확인 (GET)
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "API 서버가 정상적으로 연결되었습니다."})

# 2. 메인 이미지 가져오기 (GET)
@app.route("/image/main", methods=["GET"])
def get_main_image():
    return jsonify({"image_url": "https://example.com/main-image.jpg"})

# 3. 회원가입 (POST)
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    # 예시: 데이터 처리 로직 (DB에 저장 등)
    return jsonify({"message": "회원가입 성공", "user": data}), 201

# 4. 특정 질문 가져오기 (GET)
@app.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    # 예시: DB에서 해당 ID의 질문과 선택지 가져오기
    question = {
        "question_id": question_id,
        "question": "What is your favorite color?",
        "choices": ["Red", "Blue", "Green"]
    }
    return jsonify(question)

# 5. 질문 개수 확인 (GET)
@app.route("/questions/count", methods=["GET"])
def get_question_count():
    # 예시: DB에서 질문 개수 가져오기
    question_count = 10  # 예시 값
    return jsonify({"count": question_count})

if __name__ == "__main__":
    app.run(debug=True)

