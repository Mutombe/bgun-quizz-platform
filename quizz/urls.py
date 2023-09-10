from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('quizz/', views.quiz, name='quiz'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('category/<int:category_id>/short/', views.short_category_questions, name='short_category_questions'),
    path('category/<int:category_id>/medium/', views.medium_category_questions, name='medium_category_questions'),
    path('category/<int:category_id>/long/', views.long_category_questions, name='long_category_questions'),
    path('category/<int:category_id>/question/<int:question_id>/add_comment/', views.add_comment, name='add_comment'),
    path('submit_answer/<int:quiz_progress_id>/', views.submit_answer, name='submit_answer'),
    path('quiz_results/<int:quiz_progress_id>/', views.quiz_results, name='quiz_results'),
] 