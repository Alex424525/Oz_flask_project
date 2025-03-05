from flask import Flask 
from config import Config
from flask_migrate import Migrate
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 한글이 유니코드 이스케이프로 변환되지 않도록 설정
    app.config['JSON_AS_ASCII'] = False
    
    db.init_app(app)
    Migrate(app, db)
    
    # Blueprint 등록 (내부에서 import하여 순환 참조 방지)
    from app.routes import register_routes
    register_routes(app)
    
    return app