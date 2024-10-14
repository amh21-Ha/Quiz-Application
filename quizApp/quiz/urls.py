# quiz/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # User Authentication
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Quiz Views
    path('', views.home, name='home'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    
    # API Endpoint
    path('api/quizzes/', views.QuizListAPI.as_view(), name='quiz_list_api'),
]
