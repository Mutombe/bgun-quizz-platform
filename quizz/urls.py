from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Other URL patterns
    path('quizz/', views.quiz, name='quizz'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('category/<int:category_id>/short/', views.short_category_questions, name='short_category_questions'),
    path('category/<int:category_id>/medium/', views.medium_category_questions, name='medium_category_questions'),
    path('category/<int:category_id>/long/', views.long_category_questions, name='long_category_questions'),

]