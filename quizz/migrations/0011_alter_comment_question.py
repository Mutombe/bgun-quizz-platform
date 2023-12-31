# Generated by Django 4.2.4 on 2023-09-11 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("quizz", "0010_alter_question_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="quizz.question",
            ),
        ),
    ]
