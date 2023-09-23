# Generated by Django 4.2.4 on 2023-09-17 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("quizz", "0025_answered_delete_useranswer"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("finish_time", models.DateTimeField(blank=True, null=True)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quizz.question"
                    ),
                ),
                (
                    "selected_answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quizz.answer"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RenameField(
            model_name="quizprogress",
            old_name="questions",
            new_name="answered_questions",
        ),
        migrations.RemoveField(
            model_name="quizprogress",
            name="answer",
        ),
        migrations.AddField(
            model_name="quizprogress",
            name="answered_order",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name="Answered",
        ),
    ]
