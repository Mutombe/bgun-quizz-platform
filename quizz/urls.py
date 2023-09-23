from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/remove/<int:book_id>/', views.remove_book, name='remove_book'),
    path('books/', views.books, name='books'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('category/<int:category_id>/short/', views.short_category_questions, name='short_category_questions'),
    path('category/<int:category_id>/medium/', views.medium_category_questions, name='medium_category_questions'),
    path('category/<int:category_id>/long/', views.long_category_questions, name='long_category_questions'),
    path('random_quiz/', views.random_quiz, name='random_quiz'),
    path('add_comment/<int:question_id>/', views.add_comment, name='add_comment'),
    path('submit_answer/<int:quiz_progress_id>/', views.submit_answer, name='submit_answer'),
    path('quiz_results/<int:quiz_progress_id>/', views.quiz_results, name='quiz_results'),
    
]