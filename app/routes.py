import json
from flask import Blueprint, jsonify
from app.service.questions import get_questions
from app.service.choices import get_choices

routes = Blueprint("routes", __name__)

@routes.route("/questions", methods=["GET"])
def get_all_questions():
    """
    모든 질문과 선택지를 반환하는 API (한글 깨짐 해결)
    """
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
