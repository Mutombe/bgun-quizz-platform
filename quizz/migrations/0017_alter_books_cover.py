# Generated by Django 4.2.4 on 2023-09-14 13:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quizz", "0016_alter_books_cover"),
    ]

    operations = [
        migrations.AlterField(
            model_name="books",
            name="cover",
            field=models.ImageField(default=None, upload_to="static/files"),
        ),
    ]
