import json
from flask import Blueprint, Response

# 서비스 함수는 question_service.py에서 import합니다.
from app.routes.question_service import get_questions, get_choices  # type: ignore

questions_bp = Blueprint("questions", __name__)

@questions_bp.route("", methods=["GET"])
def get_all_questions():
    """모든 질문과 선택지를 JSON 형태로 반환 (한글 깨짐 문제 해결)"""
    questions = get_questions()
    result = []
    for question in questions:
        choices = get_choices(question["id"])
        result.append({
            "id": question["id"],
            "title": question["title"],
            "choices": choices
        })
    return json.dumps({"questions": result}, ensure_ascii=False), 200, {
        "Content-Type": "application/json; charset=utf-8"
    }

@questions_bp.route("/<int:question_id>", methods=["GET"])
def get_single_question(question_id):
    """특정 질문 하나만 JSON 형태로 반환 (한글 깨짐 문제 해결)"""
    questions = get_questions()
    question = next((q for q in questions if q["id"] == question_id), None)
    if question is None:
        return Response(
            json.dumps({"error": "해당 ID의 질문을 찾을 수 없습니다."}, ensure_ascii=False),
            status=404,
            content_type="application/json; charset=utf-8"
        )
    return Response(
        json.dumps(question, ensure_ascii=False),
        status=200,
        content_type="application/json; charset=utf-8"
    )

@questions_bp.route("/<int:question_id>/choices", methods=["GET"])
def get_question_choices(question_id):
    """특정 질문의 선택지 데이터를 JSON 형태로 반환 (한글 깨짐 문제 해결)"""
    choices = get_choices(question_id)
    if not choices:
        return Response(
            json.dumps({"error": "해당 ID의 선택지를 찾을 수 없습니다."}, ensure_ascii=False),
            status=404,
            content_type="application/json; charset=utf-8"
        )
    return Response(
        json.dumps({"question_id": question_id, "choices": choices}, ensure_ascii=False),
        status=200,
        content_type="application/json; charset=utf-8"
    )
