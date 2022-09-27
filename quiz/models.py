from django.conf import settings
from django.db import models
from django.utils import timezone


class Topic(models.Model):
    name = models.CharField(max_length=100)


class QuestionPackage(models.Model):
    name = models.CharField(max_length=100)
    # user = models.ManyToManyField(settings.AUTH_USER_MODEL)


class UserPackageRel(models.Model):
    package = models.ForeignKey(QuestionPackage, on_delete=models.CASCADE, related_name='user_rel')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='package_rel')
    first_pass_date = models.DateTimeField(default=timezone.now, blank=True)
    best_pass_date = models.DateTimeField(default=timezone.now, blank=True)
    points = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['package', 'user'],
                name="unique_package_user"
            )
        ]

    def save(self, *args, **kwargs):
        self.best_pass_date = timezone.now()
        super(UserPackageRel, self).save(*args, **kwargs)


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
