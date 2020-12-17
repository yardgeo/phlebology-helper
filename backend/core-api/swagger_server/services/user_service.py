# jwt imports
from jose import jwt

# db
from swagger_server.app import db
from swagger_server.db_models import User

# config & utils
from config import Config

# config parameters
JWT_SECRET = Config.JWT_SECRET
JWT_ALGORITHM = Config.JWT_ALGORITHM


def get_user_by_token(token):
    # check token
    token_parts = token.split()
    if len(token_parts) != 2 or token_parts[0] != 'Bearer':
        return None
    token = token_parts[-1]

    # get user
    token_info = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return db.session().query(User).filter(User.email == token_info['sub']).first()


def get_user_lifetime(token):
    # check token
    token_parts = token.split()
    if len(token_parts) != 2 or token_parts[0] != 'Bearer':
        return -1
    token = token_parts[-1]

    # get user
    token_info = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return token_info['exp'] - token_info['iat']
