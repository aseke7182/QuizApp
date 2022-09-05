from rest_framework import status
from rest_framework.views import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .messages import invalid_credentials


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def response(msg, stat, data=None):
    resp = {'message': msg}
    if data is not None:
        resp = {**resp, **data}
    return Response(resp, status=stat)


def unauthorized():
    return response(invalid_credentials, status.HTTP_401_UNAUTHORIZED)


def ok(msg="", data=None):
    if data is not None:
        return response(msg, status.HTTP_200_OK, data)
    return response(msg, status.HTTP_200_OK)
