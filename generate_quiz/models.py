from django.db import models
from file_upload.models import UploadedFile

class GeneratedQuiz(models.Model):
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    quiz_data = models.JSONField()  # Store the quiz questions and answers
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Quiz for {self.uploaded_file.original_name}"

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(GeneratedQuiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    
    def __str__(self):
        return f"Question: {self.question_text[:50]}..."
