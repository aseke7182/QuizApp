# Generated by Django 4.1 on 2022-09-06 09:30

from django.db import migrations, models
import django.db.models.deletion
import quiz.models


def general_topic(apps, schema_editor):
    Topic = apps.get_model('quiz', 'Topic')
    Topic.objects.create(name='general')


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=250)),
                ('package', models.ManyToManyField(to='quiz.questionpackage')),
                ('topic', models.ForeignKey(default=quiz.models.default_topic, null=True,
                                            on_delete=django.db.models.deletion.SET_DEFAULT, to='quiz.topic')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=250)),
                ('is_correct', models.BooleanField(default=False)),
                ('explanation', models.CharField(max_length=250)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
            ],
        ),
        migrations.RunPython(general_topic),
    ]