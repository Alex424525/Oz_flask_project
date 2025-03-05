def get_questions():
    """
    질문 데이터를 반환하는 함수 (예시 더미 데이터)
    """
    return [
        {"id": 1, "title": "What is your name?"},
        {"id": 2, "title": "What is your quest?"},
        {"id": 3, "title": "What is your favorite color?"}
    ]

def get_choices(question_id):
    """
    주어진 question_id에 해당하는 선택지 데이터를 반환하는 함수 (예시 더미 데이터)
    """
    if question_id == 1:
        return ["Alice", "Bob", "Charlie"]
    elif question_id == 2:
        return ["To seek the Holy Grail", "To explore the unknown"]
    elif question_id == 3:
        return ["Blue", "Red", "Green", "Yellow"]
    else:
        return []
