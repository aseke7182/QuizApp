from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.views import APIView

from .messages import logout_msg, login_msg
from .models import User
from .serializers import UserSerializer, RegistrationSerializer, UserLoginSerializer
from .utils import get_tokens_for_user, unauthorized, ok


def ping(request):
    return HttpResponse("Pong")


class Registration(generics.CreateAPIView):
    model = User
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)


class UsersList(generics.ListAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserInfo(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (permissions.AllowAny,)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = UserLoginSerializer(request.data).data
        user = authenticate(request, username=user['username'], password=user['password'])
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(user)
            return ok(login_msg, auth_data)
        return unauthorized()


class UserLogout(APIView):

    def post(self, request):
        logout(request)
        return ok(logout_msg)
