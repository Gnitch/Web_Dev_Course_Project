# Generated by Django 3.0.3 on 2020-07-27 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_quiz_total_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='multiple_answer',
            field=models.BooleanField(default=False),
        ),
    ]
