from app import create_app  # app/__init__.py에 정의되어 있음

application = create_app()
application.config['JSON_AS_ASCII'] = False

if __name__ == "__main__":
    application.run(debug=True)