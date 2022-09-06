from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100)


class QuestionPackage(models.Model):
    name = models.CharField(max_length=100)


def default_topic():
    try:
        topic = Topic.objects.get(id=1)
        return topic
    except Topic.DoesNotExist:
        return None


class Question(models.Model):
    content = models.CharField(max_length=250)
    topic = models.ForeignKey(Topic, on_delete=models.SET_DEFAULT, default=default_topic, null=True)
    package = models.ManyToManyField(QuestionPackage)


class Answer(models.Model):
    content = models.CharField(max_length=250)
    is_correct = models.BooleanField(default=False)
    explanation = models.CharField(max_length=250)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
