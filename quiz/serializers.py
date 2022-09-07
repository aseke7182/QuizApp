from rest_framework import serializers
from .models import QuestionPackage, Topic, Question, Answer
from .utils import validate_answers


class TopicSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Topic
        fields = ('id', 'name',)


class PackageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = QuestionPackage
        fields = ('id', 'name',)


class QuestionSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()

    class Meta:
        model = Question
        fields = ('id', 'content', 'topic',)


class PackageInfoSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, source='question_set')

    class Meta:
        model = QuestionPackage
        fields = ('id', 'name', 'questions',)


class AnswerSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=250, required=True)
    explanation = serializers.CharField(max_length=250, required=True, allow_blank=True)
    is_correct = serializers.BooleanField(required=True)

    class Meta:
        model = Answer
        fields = ('id', 'content', 'is_correct', 'explanation',)

    def validate(self, data):
        if data['is_correct'] and data['explanation'] == "":
            raise serializers.ValidationError({"explanation": "right answer should have explanation"})
        return data


class QuestionInfoSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()
    answers = AnswerSerializer(many=True, source='answer_set')

    class Meta:
        model = Question
        fields = ('id', 'content', 'topic', 'answers',)


class QuestionCreationSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=250, required=True)
    topic = TopicSerializer(read_only=True)
    topic_id = serializers.PrimaryKeyRelatedField(write_only=True, source='topic', queryset=Topic.objects.all())

    package = PackageSerializer(read_only=True, many=True)
    package_ids = serializers.PrimaryKeyRelatedField(allow_empty=False, queryset=QuestionPackage.objects.all(),
                                                     source='package', many=True, write_only=True)

    answer = AnswerSerializer(required=True, many=True)

    class Meta:
        model = Question
        fields = ('id', 'content', 'topic', 'topic_id', 'package', 'package_ids', 'answer')

    def validate(self, data):
        validate_answers(data['answer'])
        return data

    def create(self, validated_data):
        answers = validated_data.pop('answer')

        question = Question.objects.create(content=validated_data['content'], topic=validated_data['topic'])
        question.package.set(validated_data['package'])

        created_answers = []
        for answer in answers:
            ans = Answer.objects.create(question=question, **answer)
            created_answers.append(ans)

        setattr(question, 'answer', created_answers)
        return question
