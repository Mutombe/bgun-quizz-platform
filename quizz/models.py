from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

class Question(models.Model):
    image = models.ImageField(upload_to="static/files", blank=True)
    question_text = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text1 = models.CharField(max_length=200)
    answer_text2 = models.CharField(max_length=200)
    answer_text3 = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)