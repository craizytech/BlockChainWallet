from flask_jwt_extended import create_access_token

def create_jwt_token(user_id):
    return create_access_token(identity=user_id)
