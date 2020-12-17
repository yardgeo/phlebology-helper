import connexion
import six

from swagger_server.models.token_data import TokenData  # noqa: E501
from swagger_server import util

# services
import swagger_server.services.user_service as user_service


def get_user_info():  # noqa: E501
    """Get user info

     # noqa: E501


    :rtype: TokenData
    """
    token = connexion.request.headers['Authorization']

    # get user info
    user = user_service.get_user_by_token(token)
    if user is None:
        return 'Invalid token format', 401

    return TokenData(token=token,
                     access_expires_in=user_service.get_user_lifetime(token),
                     email=user.email,
                     first_name=user.first_name,
                     family_name=user.family_name,
                     role=user.role)
