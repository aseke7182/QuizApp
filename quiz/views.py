from django.http import HttpResponse
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import QuestionPackage, Topic, Question
from .serializers import PackageSerializer, TopicSerializer, QuestionCreationSerializer, PackageInfoSerializer, \
    QuestionSerializer, QuestionInfoSerializer


def ping(request):
    return HttpResponse('Pong')


class TopicAPI(generics.ListCreateAPIView):
    queryset = Topic.objects.all().order_by('id')
    serializer_class = TopicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PackageAPI(generics.ListCreateAPIView):
    queryset = QuestionPackage.objects.all().order_by('id')
    serializer_class = PackageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PackageInfoAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionPackage.objects.all()
    serializer_class = PackageInfoSerializer


class QuestionCreationAPI(views.APIView):

    def post(self, request):
        question = QuestionCreationSerializer(data=request.data)
        if question.is_valid():
            question.save()
            return Response(question.data)
        return Response(question.errors)

    def get(self, request):
        data = Question.objects.all().order_by('id')
        questions = QuestionSerializer(data, many=True)
        return Response(questions.data)


class QuestionInfoAPI(views.APIView):

    def get(self, request, pk):
        data = Question.objects.get(id=pk)
        question = QuestionInfoSerializer(data)
        return Response(question.data)
