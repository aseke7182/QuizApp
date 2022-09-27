from celery.result import AsyncResult
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .messages import logout_msg, login_msg
from .models import User
from .serializers import UserSerializer, RegistrationSerializer, UserLoginSerializer
from .tasks import send_mail
from .utils import get_tokens_for_user, unauthorized, ok


def ping(request):
    task_id = '2ccce62f-6877-443a-b3ed-2b8a748ddae8'
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result)


class Registration(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # send mail
            res = send_mail.delay(serializer.data['username'])
            print(res.id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserInfo(generics.RetrieveAPIView):
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
