# Generated by Django 3.0.3 on 2020-07-20 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='job',
        ),
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher')], default='student', max_length=10),
        ),
    ]
