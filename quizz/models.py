from django.db import models
from django.contrib.auth.models import User

class TimeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    image = models.ImageField(upload_to="static/files", blank=True)
    question_text = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return self.question_text
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user
    
class QuizProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_base = models.ForeignKey(TimeCategory, on_delete=models.CASCADE, related_name='progress', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    answered_questions = models.ManyToManyField(Question)
    score = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.user
    
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    finish_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"User: {self.user.username}, Question: {self.question.question_text}, Selected Answer: {self.selected_answer.answer_text}"
    
class Books(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to="static/files", blank=False, null=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, null=True)
    description = models.TextField()
    category = models.ManyToManyField(Category)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title