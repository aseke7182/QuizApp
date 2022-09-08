from rest_framework import serializers
from .models import QuestionPackage, Topic, Question, Answer, UserPackageRel
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
    explanation = serializers.CharField(max_length=250, required=True, allow_blank=True, write_only=True)
    is_correct = serializers.BooleanField(write_only=True, required=True)

    class Meta:
        model = Answer
        fields = ('id', 'content', 'is_correct', 'explanation',)

    def validate(self, data):
        if data['is_correct'] and data['explanation'] == "":
            raise serializers.ValidationError({"explanation": "right answer should have explanation"})
        return data


class CorrectAnswersSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ('content', 'is_correct', 'explanation', 'question',)


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


class QuestionSubmitSerializer(serializers.Serializer):
    answers = serializers.ListSerializer(child=serializers.IntegerField(), required=True, write_only=True)
    score = serializers.IntegerField(read_only=True)
    right_answers = serializers.ListSerializer(child=CorrectAnswersSerializer(), read_only=True)

    def validate(self, data):
        answers = list(set(data['answers']))
        package_id = self.context['package_id']
        questions = QuestionPackage.objects.get(id=package_id).question_set.all()
        question_count = questions.count()
        if question_count > len(answers):
            raise serializers.ValidationError({"answers": "not all questions answered"})
        elif question_count < len(answers):
            raise serializers.ValidationError({"answers": "too many arguments"})

        right_answers = set()
        for answer in answers:
            answer_in_question_set = False
            for question in questions:
                question_answers = question.answer_set.all()
                for q in question_answers:
                    if q.is_correct:
                        right_answers.add(q)
                    if q.id == answer:
                        answer_in_question_set = True
            if not answer_in_question_set:
                raise serializers.ValidationError({"answers": "some answers are not from this package"})

        data.update({'right_answers': list(right_answers)})
        return data

    def create(self, validated_data):
        package_id = self.context['package_id']
        user = self.context['user']
        score = 0

        answers = Answer.objects.filter(id__in=validated_data['answers'])
        for ans in answers:
            if ans.is_correct:
                score += 1

        # TODO: Somehow to do it more efficiently?
        user_package_rel, created = UserPackageRel.objects.get_or_create(package_id=package_id, user=user)
        now_score = 0
        if not created:
            now_score = user_package_rel.points
        user_package_rel.points = max(score, now_score)
        user_package_rel.save()

        validated_data['score'] = score
        return validated_data

    def update(self, instance, validated_data):
        """
        No such functionality yet
        :param instance:
        :param validated_data:
        :return:
        """
        return validated_data
