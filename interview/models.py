# interviews/models.py

from django.db import models
from django.contrib.auth.models import User

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.TextField()
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    answer = models.TextField()  # New field to store the correct answer

    def __str__(self):
        return self.question_text

class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_response = models.TextField()
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.question.question_text[:50]}"
