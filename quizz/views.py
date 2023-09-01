from django.shortcuts import render

def homepage(request):
    return render(request, 'quizz/home.html')

# views.py

from django.shortcuts import render, redirect
from .models import Category, Question

def quiz_view(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category)
    total_questions = questions.count()
    
    current_question_index = request.session.get('current_question_index', 0)
    current_question = questions[current_question_index]
    
    if request.method == 'POST':
        # Process the submitted answer
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