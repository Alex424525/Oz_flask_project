import json
from flask import Blueprint, jsonify , Response

# 질문과 선택지 데이터를 가져오는 함수들 import함
from app.service.questions import get_questions
from app.service.choices import get_choices

# Flask Blueprint 설정
routes = Blueprint("routes", __name__)

# 기존 기능: 모든 질문과 선택지를 반환하는 API(한글 깨짐 문제 해결)
@routes.route("/questions", methods=["GET"])
def get_all_questions():
    # 모든 질문과 선택지를 JSON 형태로 반환하는 API
    questions = get_questions()
    result = []

    for question in questions:
        choices = get_choices(question["id"])
        result.append({
            "id": question["id"],
            "title": question["title"],
            "choices": choices
        })

    return json.dumps({"questions": result}, ensure_ascii=False), 200, {"Content-Type": "application/json; charset=utf-8"}

# 새로운 기능: 특정 질문 하나만 가져오는 API(한글 깨짐 문제 해결)
@routes.route("/questions/<int:question_id>" , methods=["GET"])
def get_single_question(question_id):
    # 특정 질문 하나만 JSON 형태로 반환하는 API
    questions = get_questions()
    question = next((q for q in questions if q["id"] == question_id), None)

    if question is None:
        return Response(json.dumps({"error": "해당 ID의 질문을 찾을 수 없습니다."}, ensure_ascii=False), 
                        status=404, content_type="application/json; charset=utf-8")
    
    return Response(json.dumps(question, ensure_ascii=False), 
                    status=200, content_type="application/json; charset=utf-8")

# 새로운 기능: 특정 질문의 선택지만 가져오는 API(한글 깨짐 문제 해결)
@routes.route("/questions/<int:question_id>/choices" , methods=["GET"])
def get_question_choices(question_id):
    # 특정 질문 하나만 JSON 형태로 반환하는 API
    choices = get_choices(question_id)

    if not choices:
        return Response(json.dumps({"error": "해당 ID의 선택지를 찾을 수 없습니다."}, ensure_ascii=False), 
                        status=404, content_type="application/json; charset=utf-8")

    return Response(json.dumps({"question_id": question_id, "choices": choices}, ensure_ascii=False), 
                    status=200, content_type="application/json; charset=utf-8")