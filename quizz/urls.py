from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Other URL patterns
    path('quizz/', views.quiz, name='quizz'), 

]