class Config:
    SECRET_KEY = 'your_secret_key'
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_HOST = 'localhost'
    DB_USER = 'postgres'
    DB_PASSWORD = 'password'
    DB_PORT = '5432'
