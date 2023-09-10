# Generated by Django 4.2.4 on 2023-09-10 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("quizz", "0009_quizprogress_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="quizz.category",
            ),
        ),
    ]
