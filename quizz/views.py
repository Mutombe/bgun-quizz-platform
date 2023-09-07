from django.shortcuts import render, redirect
from .models import Category, Comment, Question,QuizProgress, TimeCategory
from django.http import HttpResponseNotAllowed
from django.db.models import Value, IntegerField
from django.core.paginator import Paginator
from datetime import datetime


def homepage(request):
    categories = Category.objects.all()
    return render(request, 'quizz/home.html',{'categories': categories})

def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'quizz/category_detail.html', {'category': category})

def category_questions(request, category_id):
    category = Category.objects.get(id=category_id)
    time_category = category.time_category
    questions = Question.objects.filter(category=category)
    context = {
        'category': category, 
        'questions': questions,
        'time_category': time_category,
    }
    return render(request, 'quizz/category_detail.html', context)


def short_category_questions(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category).order_by('?')[:10]
    total_questions = questions.count()
    paginator = Paginator(questions, 1)  
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        for question in page_obj:
            selected_option_id = request.POST.get('selected_option')
            if selected_option_id in question.answer_set.values_list('id', flat=True):
                selected_option = question.answer_set.get(id=selected_option_id)
                
                if selected_option.is_correct:
                    quiz_progress, created = QuizProgress.objects.get_or_create(user=request.user, category=category, time_category=time_category)
                    quiz_progress.score += 1
                    
                    
                    
                next_index = page_obj.index(question) + 1
                if next_index < len(questions):
                    next_question = questions[next_index]
                else: 
                    next_index = None
                if next_question:
                    return redirect('short_category_questions', category_id=category_id,  page=next_question.number)
                else:
                    quiz_progress.finish_time = datetime.now()
                    quiz_progress.save()
                    return redirect('quiz_summary', category_id=category_id, time_category='short')

    return render(request, 'quizz/shorts.html', {'category': category, 'questions': questions, 'total_questions': total_questions, 'page_obj': page_obj})

def medium_category_questions(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category).order_by('?')[:50]
    return render(request, 'quizz/medium.html', {'category': category, 'questions': questions})

def long_category_questions(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category).order_by('?')[:100]
    return render(request, 'quizz/long.html', {'category': category, 'questions': questions})

def quiz_summary(request, category_id, time_category):
    category = Category.objects.get(id=category_id)
    time_category = TimeCategory.objects.get(name=time_category)
    total_questions = Question.objects.filter(category=category, time_category=time_category).count()
    quiz_progress = QuizProgress.objects.get(user=request.user, category=category, time_category=time_category)

    score = quiz_progress.score
    date_time = quiz_progress.finish_time
    
    return render(request, 'quizz/quiz_summary.html', {'category': category, 'time_category': time_category, 'total_questions': total_questions, 'score': score,  'date_time': date_time})

def add_comment(request, category_id, question_id):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        question = Question.objects.get(id=question_id)
        category = Category.objects.get(id=category_id)

        # Create a new Comment object and save it to the database
        new_comment = Comment(user=request.user, question=question, content=comment)
        new_comment.save()
        #return redirect('question_details', category_id=category_id, question_id=question_id)
    # Handle the case when the request method is not POST (e.g., GET request)
    return HttpResponseNotAllowed(['POST'])

def quiz(request):
    return render(request, 'quizz/quiz.html')