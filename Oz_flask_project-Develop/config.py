class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://oz_flask:P%40ssw0rd%21@localhost/Ozdatabase"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 5
    SQLALCHEMY_POOL_RECYCLE = 1800
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "oz_form_secret"
    UPLOAD_FOLDER = "static/images"
