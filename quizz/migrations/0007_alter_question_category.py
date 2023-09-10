# Generated by Django 4.2.4 on 2023-09-10 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("quizz", "0006_alter_answer_question"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="category",
                to="quizz.category",
            ),
        ),
    ]
