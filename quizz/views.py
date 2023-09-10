from .models import Category, Comment, UserAnswer, TimeCategory, QuizProgress, Question, Answer
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages


def homepage(request):
    categories = Category.objects.all()
    return render(request, "quizz/home.html", {"categories": categories})

def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, "quizz/category_detail.html", {"category": category})

@login_required
def short_category_questions(request, category_id):
    category = Category.objects.get(pk=category_id)
    # Get the category and 10 random questions from a certain category
    questions = Question.objects.filter(category=category).order_by("?")[:10]
    # Create a new quiz progress object for the user and the category
    
    paginator = Paginator(questions, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    quiz_progress = QuizProgress.objects.create(
        user=request.user, category=category, start_time=timezone.now()
    )
    initial_score =  0
    return render(
        request,
        "quizz/shorts.html",
        {"quiz_progress": quiz_progress, "questions": questions, "page_obj": page_obj, "initial_score": initial_score},
    )

def medium_category_questions(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category).order_by("?")[:50]
    
    paginator = Paginator(questions, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    quiz_progress = QuizProgress.objects.create(
        user=request.user, category=category, start_time=timezone.now()
    )
    
    return render(
        request, "quizz/medium.html", {"quiz_progress": quiz_progress, "questions": questions, "page_obj": page_obj, "category": category, "questions": questions}
    )


def long_category_questions(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category).order_by("?")[:100]
    
    paginator = Paginator(questions, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    quiz_progress = QuizProgress.objects.create(
        user=request.user, category=category, start_time=timezone.now()
    )
    return render(
        request, "quizz/long.html", {"quiz_progress": quiz_progress, "questions": questions, "page_obj": page_obj, "category": category, "questions": questions}
    )


def submit_answer(request, quiz_progress_id):
    # Get the quiz progress from the request
    quiz_progress = QuizProgress.objects.get(pk=quiz_progress_id)

    try:
        # Get the selected answer from the request
        selected_answer_id = request.POST["selected_answer"]
        selected_answer = Answer.objects.get(pk=selected_answer_id)

        # Update the score and the answered questions of the quiz progress
        if selected_answer.is_correct:
            quiz_progress.score += 1
        else:
            if "previous" in request.POST and selected_answer.question in quiz_progress.answered_questions.all():
                quiz_progress.score -= 1

        current_question = selected_answer.question
        quiz_progress.answered_questions.add(current_question)

        # Get the next question from the same category that is not answered yet
        next_question = get_next_question(current_question, quiz_progress)

        # If there is a next question, redirect to it
        if next_question and "next" in request.POST:
            return redirect(reverse("short_category_questions", kwargs={"category_id": quiz_progress.category.id}) + "?page=2")

        # Otherwise, save the end time of the quiz progress and redirect to the results page
        elif "submit" in request.POST or not next_question:
            quiz_progress.end_time = timezone.now()
            quiz_progress.save()
            return redirect("quiz_results", quiz_progress.id)

    except MultiValueDictKeyError:
        # Handle the case when no answer is selected
        error_message = "Please select an answer."
        messages.error(request, error_message)
        return redirect(request.META.get('HTTP_REFERER', 'short_category_questions'))
    
def get_next_question(current_question, quiz_progress):
    # Get all the questions from the same category as the current question
    category_questions = current_question.category.questions.all()
    # Get the ids of the questions that are already answered by the user
    answered_question_ids = quiz_progress.answered_questions.values_list(
        "id", flat=True
    )
    # Filter out the answered questions and get the first one from the remaining ones
    unanswered_questions = category_questions.exclude(id__in=answered_question_ids)
    next_question = unanswered_questions.first()

    return next_question


def quiz_results(request, quiz_progress_id):
  # Get the quiz progress object by its id
  quiz_progress = QuizProgress.objects.get(pk=quiz_progress_id)

  # Get the total number of questions in the quiz
  total_questions = quiz_progress.answered_questions.count()
  category = quiz_progress.category
  # Get the score and the time taken by the user
  score = quiz_progress.score
  time_taken = quiz_progress.end_time - quiz_progress.start_time

  # Calculate the percentage score and format it as a string
  percentage_score_first = (score / total_questions) * 100
  percentage_score = f"{percentage_score_first:.2f}%"

  # Get the list of questions and answers from the quiz progress object
  questions = quiz_progress.answered_questions.all()


  # Zip the questions and answers together and convert them to a list
  combined = list(zip(questions))

  # Render the results template with the context variables
  return render(request, 'quizz/results.html', {
    'quiz_progress': quiz_progress,
    'total_questions': total_questions,
    'score': score,
    'category': category,
    'time_taken': time_taken,
    'percentage_score': percentage_score,
    'percentage_score_first': percentage_score_first,
    'combined': combined
  })


def add_comment(request, category_id, question_id):
    if request.method == "POST":
        comment = request.POST.get("comment")
        question = Question.objects.get(id=question_id)
        category = Category.objects.get(id=category_id)

        # Create a new Comment object and save it to the database
        new_comment = Comment(user=request.user, question=question, content=comment)
        new_comment.save()
        # return redirect('question_details', category_id=category_id, question_id=question_id)
    # Handle the case when the request method is not POST (e.g., GET request)
    return HttpResponseNotAllowed(["POST"])


def quiz(request):
    return render(request, "quizz/quiz.html")
