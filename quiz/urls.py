from django.urls import path
from .views import ping, PackageAPI, PackageInfoAPI, TopicAPI, QuestionCreation

urlpatterns = [
    path('ping', ping),
    path('packages', PackageAPI.as_view()),
    path('packages/<int:pk>', PackageInfoAPI.as_view()),
    path('topics', TopicAPI.as_view()),
    path('questions', QuestionCreation.as_view())
]
