from django.contrib.auth.models import User
from quizz.models import Category
from django.db import models



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    location = models.CharField(max_length=100)
    interests = models.ManyToManyField(Category)
    email = models.EmailField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username