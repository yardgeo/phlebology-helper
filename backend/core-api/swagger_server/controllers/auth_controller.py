import time
import connexion
import six
import hashlib
import os
import random

# util imports
from swagger_server import util

# db imports
from swagger_server.models.token_data import TokenData  # noqa: E501
from swagger_server.models.user_data import UserData  # noqa: E501
from swagger_server.app import db
from swagger_server.db_models import User

# services imports
from swagger_server.services.email_service import send_recovery_letter

from werkzeug.exceptions import Unauthorized

from jose import JWTError, jwt

from config import Config

JWT_ISSUER = Config.JWT_ISSUER
JWT_SECRET = Config.JWT_SECRET
JWT_LIFETIME_SECONDS = Config.JWT_LIFETIME_SECONDS
JWT_ALGORITHM = Config.JWT_ALGORITHM
NUMBER_HASH_ITERATIONS = Config.NUMBER_HASH_ITERATIONS
HASH_ALGORITHM = Config.HASH_ALGORITHM
RECOVERY_CODE_LEFT_RANGE = Config.RECOVERY_CODE_LEFT_RANGE
RECOVERY_CODE_RIGHT_RANGE = Config.RECOVERY_CODE_RIGHT_RANGE


def change_password(email, newPassword, recoveryCode):  # noqa: E501
    """User change password

     # noqa: E501

    :param email: User email
    :type email: str
    :param newPassword: User new password
    :type newPassword: str
    :param recoveryCode: Recovery code from recovery letter
    :type recoveryCode: str

    :rtype: None
    """

    user = db.session().query(User).filter(User.email == email).first()

    # check user exist
    if user is None:
        return 'User with email {email} not found'.format(email=email), 404

    # check user has code
    if user.recovery_status != 2:
        return 'User with email {email} need to call recovery' \
               ' method and check recovery code first'.format(email=email), 405

    # check recovery code
    recovery_key = hashlib.pbkdf2_hmac(HASH_ALGORITHM,
                                       str(recoveryCode).encode('utf-8'),
                                       user.salt,
                                       NUMBER_HASH_ITERATIONS)
    if recovery_key != user.recovery_key:
        return 'Wrong recovery code {code} for user with email {email}' \
                   .format(code=recoveryCode, email=email), 403

    # save new password
    user.key = hashlib.pbkdf2_hmac(HASH_ALGORITHM,
                                   str(newPassword).encode('utf-8'),
                                   user.salt,
                                   NUMBER_HASH_ITERATIONS)

    # update recovery status
    user.recovery_status = 0
    db.session().commit()

    return 'Password changed successfully!'


def check_recovery_password(email, recoveryCode):  # noqa: E501
    """Recovery password check

     # noqa: E501

    :param email: User email
    :type email: str
    :param recoveryCode: Recovery code from recovery letter
    :type recoveryCode: str

    :rtype: None
    """

    user = db.session().query(User).filter(User.email == email).first()

    # check user exist
    if user is None:
        return 'User with email {email} not found'.format(email=email), 404

    # check user has code
    if user.recovery_status != 1:
        return 'User with email {email} need to call recovery method first'.format(email=email), 405

    # check recovery code
    recovery_key = hashlib.pbkdf2_hmac(HASH_ALGORITHM,
                                       str(recoveryCode).encode('utf-8'),
                                       user.salt,
                                       NUMBER_HASH_ITERATIONS)
    if recovery_key != user.recovery_key:
        return 'Wrong recovery code {code} for user with email {email}' \
                   .format(code=recoveryCode, email=email), 403

    # update recovery status
    user.recovery_status = 2
    db.session().commit()

    return 'Correct recovery code!'


def login(body):  # noqa: E501
    """User login

     # noqa: E501

    :param body: User data
    :type body: dict | bytes

    :rtype: TokenData
    """

    # parse body
    if body is None:
        return 'Request body not in json format!', 400

    # get data
    email = body['email']
    password = body['password']

    user = db.session().query(User).filter(User.email == email).first()

    # check user exist
    if user is None:
        return 'User with email {email} not found'.format(email=email), 404

    # check password
    key = hashlib.pbkdf2_hmac(HASH_ALGORITHM, password.encode('utf-8'), user.salt, NUMBER_HASH_ITERATIONS)
    if key != user.key:
        return 'Wrong password for user with email {email}'.format(email=email), 403

    # create token
    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": user.email,
    }

    # login user
    user.log_out = False
    db.session().commit()

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return TokenData(token=token,
                     access_expires_in=JWT_LIFETIME_SECONDS,
                     email=user.email,
                     first_name=user.first_name,
                     family_name=user.family_name,
                     role=user.role)


def logout():  # noqa: E501
    """User logout

     # noqa: E501


    :rtype: None
    """
    token = connexion.request.headers['Authorization']

    # check token
    token_parts = token.split()
    if len(token_parts) != 2 or token_parts[0] != 'Bearer':
        return 'Invalid token format', 401
    token = token_parts[-1]

    # logout
    token_info = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    user = db.session().query(User).filter(User.email == token_info['sub']).first()
    user.log_out = True
    db.session().commit()

    return 'Successfully logout!'


def recovery_password(email):  # noqa: E501
    """Recovery password

     # noqa: E501

    :param email: User email
    :type email: str

    :rtype: None
    """

    user = db.session().query(User).filter(User.email == email).first()

    # check user exist
    if user is None:
        return 'User with email {email} not found'.format(email=email), 404

    # create recovery code
    recovery_code = random.randint(RECOVERY_CODE_LEFT_RANGE, RECOVERY_CODE_RIGHT_RANGE)

    # send recovery letter
    send_recovery_letter(email, recovery_code, user.first_name)

    # save recovery code
    user.recovery_status = 1
    user.recovery_key = hashlib.pbkdf2_hmac(HASH_ALGORITHM,
                                            str(recovery_code).encode('utf-8'),
                                            user.salt,
                                            NUMBER_HASH_ITERATIONS)
    db.session().commit()

    return 'Recovery letter has been sending'


def decode_token(token, required_scopes=None):  # noqa: E501
    try:
        # check Bearer token
        token_parts = token.split()
        if len(token_parts) != 2 or token_parts[0] != 'Bearer':
            raise JWTError('Invalid token format')
        token = token_parts[-1]

        # get token_info
        token_info = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = db.session().query(User).filter(User.email == token_info['sub']).first()

        # check user logout
        if user is None or user.log_out:
            raise JWTError('User has been logout')
        else:
            return token_info

    except JWTError as e:
        six.raise_from(Unauthorized, e)


def _current_timestamp() -> int:
    return int(time.time())
