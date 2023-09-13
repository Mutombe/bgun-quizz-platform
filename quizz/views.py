import re
import random

from quizz.forms import BooksForm, CommentForm
from .models import Books, Category, Comment, UserAnswer, TimeCategory, QuizProgress, Question, Answer
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.http import HttpResponseRedirect

def homepage(request):
    categories = Category.objects.all()
    return render(request, "quizz/home.html", {"categories": categories})

def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, "quizz/category_detail.html", {"category": category})

@login_required(login_url="login")
def short_category_questions(request, category_id):
    category = Category.objects.get(pk=category_id)
    time_base = TimeCategory.objects.get(name='short')
    # Get the category and 10 random questions from a certain category
    questions = Question.objects.filter(category=category).order_by("?")[:10]
    # Create a new quiz progress object for the user and the category
    
    paginator = Paginator(questions, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    comments = Comment.objects.filter(question__in=page_obj.object_list).order_by('-created_at')
    quiz_progress = QuizProgress.objects.create(
        user=request.user, time_base=time_base, category=category, start_time=timezone.now()
    )
    return render(
        request,
        "quizz/shorts.html",
        {"quiz_progress": quiz_progress, "questions": questions, "page_obj": page_obj, "comments": comments},
    )

@login_required(login_url="login")
def medium_category_questions(request, category_id):
    category = Category.objects.get(id=category_id)
    time_base = TimeCategory.objects.get(name='medium')
    questions = Question.objects.filter(category=category).order_by("?")[:50]
    
    paginator = Paginator(questions, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    comments = Comment.objects.filter(question__in=page_obj.object_list).order_by('-created_at')
    quiz_progress = QuizProgress.objects.create(
        user=request.user, time_base=time_base, category=category, start_time=timezone.now()
    )
    
    return render(
        request, "quizz/medium.html", {"quiz_progress": quiz_progress, "questions": questions, "page_obj": page_obj, "category": category, "comments": comments}
    )

@login_required(login_url="login")
def long_category_questions(request, category_id):
    category = Category.objects.get(id=category_id)
    time_base = TimeCategory.objects.get(name='long')
    questions = Question.objects.filter(category=category).order_by("?")[:100]
    
    paginator = Paginator(questions, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    comments = Comment.objects.filter(question__in=page_obj.object_list).order_by('-created_at')
    quiz_progress = QuizProgress.objects.create(
        user=request.user, time_base=time_base, category=category, start_time=timezone.now()
    )
    return render(
        request, "quizz/long.html", {"quiz_progress": quiz_progress, "questions": questions, "page_obj": page_obj, "category": category, "comments": comments}
    )

def random_quiz(request):
    categories = Category.objects.all()
    time_categories = TimeCategory.objects.all()

    random_category = random.choice(categories)
    random_time_category = random.choice(time_categories)

    url = ""

    if random_time_category.name == "short":
        url = f"/category/{random_category.id}/"
    elif random_time_category.name == "medium":
        url = f"/category/{random_category.id}/"
    elif random_time_category.name == "long":
        url = f"/category/{random_category.id}/"

    return redirect(url)

@login_required(login_url="login")
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

        #if user is adding comments
        if 'comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.question = current_question  # Assuming current_question is defined above
                new_comment.user = request.user
                new_comment.save()
                
        # If there is a next question, redirect to it
        if next_question and "next_page" in request.POST:
            #return redirect(reverse("short_category_questions", kwargs={"category_id": quiz_progress.category.id}) + "?page=2")
            if quiz_progress.time_base.name == "short":
                return redirect(reverse("short_category_questions", kwargs={"category_id": quiz_progress.category.id}) + f"?page={next_question.id}")
            elif quiz_progress.time_base.name == "medium":
                return redirect(reverse("medium_category_questions", kwargs={"category_id": quiz_progress.category.id}) + f"?page={next_question.id}")
            elif quiz_progress.time_base.name == "long":
                return redirect(reverse("long_category_questions", kwargs={"category_id": quiz_progress.category.id}) + f"?page={next_question.id}")
        # Otherwise, save the end time of the quiz progress and redirect to the results page
        elif "submit" in request.POST or not next_question:
            quiz_progress.end_time = timezone.now()
            quiz_progress.save()
            return redirect("quiz_results", quiz_progress.id)

    except MultiValueDictKeyError:
        # Handle the case when no answer is selected
        error_message = "Please select an answer."
        messages.error(request, error_message)
        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect("/")
    
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

@login_required(login_url="login")
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


def jadd_comment(request, category_id, question_id):
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



@login_required(login_url="login")
def zadd_comment(request, pk):
    if request.method == "POST":
        question = Question.objects.get(pk=pk)
        comment_text = request.POST.get("comment_form")
        
        if comment_text:
            comment = Comment(question=question, user=request.user, comment_text=comment_text)
            comment.save()
    
    redirect_url = request.META.get("HTTP_REFERER")
    return redirect(redirect_url)

@login_required(login_url="login")
def add_comment(request, pk):
    if request.method == "POST":
        question = Question.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.question = question
            new_comment.user = request.user
            new_comment.save()
    
    redirect_url = request.META.get("HTTP_REFERER")
    return redirect(redirect_url)

def books(request):
    books = Books.objects.all()
    return render(request, "quizz/books.html", {'books':books})

@login_required
def edit_book(request):
    user = request.user
    book, created = Books.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = BooksForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = BooksForm(instance=book)
    
    return render(request, 'quizz/edit_book.html', {'form': form})

def book_add(request):
    if request.method == "POST":
        form = BooksForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            messages.success(request, "Book added successfully")
            return redirect("dash")
    else:
        form = BooksForm()
    return render(request, "quizz/book_add.html", {"form": form})