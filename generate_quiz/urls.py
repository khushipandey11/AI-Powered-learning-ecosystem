# generate_quiz/urls.py
from django.urls import path
from . import views

app_name = "generate_quiz"

urlpatterns = [
    path('<int:uploaded_file_id>/', views.generate_quiz, name='generate_quiz'),
    path('export/<int:quiz_id>/', views.export_quiz, name='export_quiz'),
]