choices_data = {
    1: [
        {"text": "거의 없음", "score": 1},
        {"text": "가끔 있음", "score": 2},
        {"text": "자주 있음", "score": 3},
        {"text": "매일 있음", "score": 4}
    ],
    2: [
        {"text": "금방 잊고 넘어감", "score": 1},
        {"text": "음악을 듣거나 운동함", "score": 2},
        {"text": "친구나 가족에게 털어놓음", "score": 3},
        {"text": "혼자 끙끙 앓는다", "score": 4}
    ],
    3: [
        {"text": "충분한 수면을 취함", "score": 1},
        {"text": "가끔 늦게 잠", "score": 2},
        {"text": "자주 늦게 잠", "score": 3},
        {"text": "매일 못 잠", "score": 4}
    ],
    4: [
        {"text": "침착하게 해결방법을 찾음", "score": 1},
        {"text": "당황하지만 해결하려고 노력함", "score": 2},
        {"text": "해결방법을 찾지 못하고 쉽게 지침", "score": 3},
        {"text": "심한 압박감을 느끼며 걱정함", "score": 4}
    ]
}

def get_choices(question_id):
    return choices_data.get(question_id, [])
