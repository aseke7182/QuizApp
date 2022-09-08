from django.urls import path
from .views import ping, PackageAPI, PackageInfoAPI, TopicAPI, QuestionCreationAPI, QuestionInfoAPI, SubmitScoreAPI

urlpatterns = [
    path('ping', ping),
    path('packages', PackageAPI.as_view()),
    path('packages/<int:pk>', PackageInfoAPI.as_view()),
    path('packages/<int:pk>/submit', SubmitScoreAPI.as_view()),
    path('topics', TopicAPI.as_view()),
    path('questions', QuestionCreationAPI.as_view()),
    path('questions/<int:pk>', QuestionInfoAPI.as_view()),
]
