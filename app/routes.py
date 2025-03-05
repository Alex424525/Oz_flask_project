import json
from flask import Blueprint, jsonify, request, session, Response
from app.service.questions import get_questions
from app.service.choices import get_choices  # 선택지 가져오기

# Flask Blueprint 생성
routes = Blueprint("routes", __name__)

# 모든 질문을 반환하는 API
@routes.route("/questions", methods=["GET"])
def get_all_questions():
    questions = get_questions()
    result = []

    for question in questions:
        choices = get_choices(question["id"])  # 선택지 가져오기
        result.append({
            "id": question["id"],
            "title": question["title"],
            "choices": choices
        })

    return Response(json.dumps({"questions": result}, ensure_ascii=False), 
                    status=200, content_type="application/json; charset=utf-8")

# 특정 질문 반환 API
@routes.route("/questions/<int:question_id>", methods=["GET"])
def get_single_question(question_id):
    questions = get_questions()
    question = next((q for q in questions if q["id"] == question_id), None)

    if question is None:
        return Response(json.dumps({"error": "해당 ID의 질문을 찾을 수 없습니다."}, ensure_ascii=False),
                        status=404, content_type="application/json; charset=utf-8")

    choices = get_choices(question_id)

    return Response(json.dumps({
        "id": question["id"],
        "title": question["title"],
        "choices": choices
    }, ensure_ascii=False), 
                    status=200, content_type="application/json; charset=utf-8")

# 사용자의 선택을 저장하는 API
@routes.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.json
    score = data.get("score", 0)

    if "total_score" not in session:
        session["total_score"] = 0  # 세션 초기화

    session["total_score"] += score  # 점수 합산

    print(f"현재 총점 (디버깅): {session['total_score']}")  # 터미널에서 점수 확인용 로그

    return jsonify({"message": "점수가 추가되었습니다.", "total_score": session["total_score"]})




# 스트레스 점수 결과 반환 API
@routes.route("/get_result", methods=["GET"])
def get_result():
    total_score = session.get("total_score", 0)

    print(f"최종 점수 (디버깅): {total_score}")  # 최종 점수 확인 로그 추가

    if total_score <= 4:
        result = "스트레스 프리형: 스트레스가 거의 없어요!"
    elif total_score <= 8:
        result = "일반적인 스트레스형: 적절한 휴식이 필요해요."
    elif total_score <= 12:
        result = "누적된 스트레스형: 스트레스 해소 방법이 필요해요."
    else:
        result = "심각한 스트레스형: 전문가의 도움이 필요할 수 있어요."

    return jsonify({"total_score": total_score, "result": result})




from flask import Blueprint, render_template, session

@routes.route("/")
def home():
    session["total_score"] = 0  # 점수 초기화
    return render_template("index.html")
