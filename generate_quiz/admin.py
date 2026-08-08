from django.contrib import admin
from .models import GeneratedQuiz, QuizQuestion

@admin.register(GeneratedQuiz)
class GeneratedQuizAdmin(admin.ModelAdmin):
    list_display = ['uploaded_file', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text', 'correct_answer']
    list_filter = ['correct_answer', 'quiz__created_at']
