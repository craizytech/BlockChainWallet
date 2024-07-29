import datetime

class Config:
    SECRET_KEY = 'your_secret_key'
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=24)
    DB_USER = 'postgres'
    DB_PASSWORD = 'password'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
