from rest_framework import serializers


def validate_answers(answers):
    right_answers = 0
    if len(answers) < 2:
        raise serializers.ValidationError({"answer": "should be at least two variants"})
    for answer in answers:
        if answer['is_correct']:
            right_answers += 1
    if right_answers != 1:
        raise serializers.ValidationError({"answers": "Must be one correct answer"})
