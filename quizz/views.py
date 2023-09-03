from django.shortcuts import render, redirect
from .models import Category, Question,QuizProgress, TimeCategory


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
    return render(request, 'quizz/shorts.html', {'category': category, 'questions': questions})

def medium_category_questions(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category).order_by('?')[:50]
    return render(request, 'quizz/medium.html', {'category': category, 'questions': questions})

def long_category_questions(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category).order_by('?')[:100]
    return render(request, 'quizz/long.html', {'category': category, 'questions': questions})

def submit_answer(request, category_id, time_category, question_id):
    if request.method == 'POST':
        selected_option_id = request.POST.get('selected_option')
        question = Question.objects.get(id=question_id)
        selected_option = question.answer_set.get(id=selected_option_id)
        
        if selected_option.is_correct:
            # Retrieve or create the quiz progress for the user
            quiz_progress, created = QuizProgress.objects.get_or_create(user=request.user, category=question.category, time_category=time_category)
            quiz_progress.score += 1
            quiz_progress.save()

        return redirect('next_question', category_id=category_id, time_category=time_category, question_id=question_id)
    
def quiz_summary(request, category_id, time_category):
    category = Category.objects.get(id=category_id)
    time_category = TimeCategory.objects.get(name=time_category)
    total_questions = Question.objects.filter(category=category, time_category=time_category).count()
    score = request.session.get('score', 0)

    # Clear the session data to start a new quiz
    request.session.flush()

    # Render the template for quiz summary and pass the necessary context data
    return render(request, 'quiz_summary.html', {'category': category, 'time_category': time_category, 'total_questions': total_questions, 'score': score})

def quiz_view(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category)
    total_questions = questions.count()
    
    current_question_index = request.session.get('current_question_index', 0)
    current_question = questions[current_question_index]
    
    if request.method == 'POST':
        selected_answer = request.POST.get('selected_answer')
        is_correct = (selected_answer == current_question.correct_answer)
        # Save the user's answer or perform any other necessary actions
        
        # Update the current question index
        current_question_index += 1
        if current_question_index >= total_questions:
            # User has completed all questions, redirect to a summary page or result page
            return redirect('quiz_summary')
        
        # Save the updated current question index in session
        request.session['current_question_index'] = current_question_index
        return redirect('quiz_view', category_id=category_id)
    
    context = {
        'category': category,
        'current_question': current_question,
        'total_questions': total_questions,
        'current_question_index': current_question_index,
    }
    return render(request, 'quiz.html', context)

def quiz(request):
    return render(request, 'quizz/quiz.html')