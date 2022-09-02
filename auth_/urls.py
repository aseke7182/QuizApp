from django.contrib import admin
from django.urls import path
from auth_.views import ping

urlpatterns = [
    path('ping/', ping),
]
