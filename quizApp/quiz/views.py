from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Quiz, Question, Option, Result
from rest_framework import generics
from .serializers import QuizSerializer

# User Registration View
def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})

# User Login View
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'quiz/login.html', {'form': form})

# User Logout View
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

# Home View (Displays all quizzes)
@login_required
def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/home.html', {'quizzes': quizzes})

# Take Quiz View (Displays quiz questions)
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions})

# Submit Quiz View (Handles quiz submission and scoring)
@login_required
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = 0
        total = quiz.question_set.count()
        for question in quiz.question_set.all():
            selected_option_id = request.POST.get(str(question.id))
            if selected_option_id:
                try:
                    selected_option = Option.objects.get(id=int(selected_option_id))
                    if selected_option.is_correct:
                        score += 1
                except Option.DoesNotExist:
                    pass
        Result.objects.create(user=request.user, quiz=quiz, score=score)
        return JsonResponse({'score': score, 'total': total})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# REST API View for Listing Quizzes
class QuizListAPI(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
