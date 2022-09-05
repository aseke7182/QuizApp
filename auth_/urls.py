from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import ping, UsersList, UserInfo, Registration, UserLogin, UserLogout

urlpatterns = [
    path('ping', ping),
    path('users', UsersList.as_view()),
    path('users/<int:pk>', UserInfo.as_view()),
    path('signup', Registration.as_view()),
    path('login', UserLogin.as_view()),
    path('logout', UserLogout.as_view()),
    path('refresh', jwt_views.TokenRefreshView.as_view())
]
