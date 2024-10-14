from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    time_limit = models.IntegerField(default=30)  # Time in seconds

    def __str__(self):
        return self.question_text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"
