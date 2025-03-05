def register_routes(app):
    # 내부에서 각 모듈을 import하여 순환 참조 문제 방지
    from app.routes import users, question, images_answers
    app.register_blueprint(users.users_blp, url_prefix="/users")
    app.register_blueprint(question.questions_bp, url_prefix="/questions")
    app.register_blueprint(images_answers.images_bp, url_prefix="/")
    return app