# generate_notes/urls.py
from django.urls import path
from . import views

app_name = "generate_notes"

urlpatterns = [
    path('<int:uploaded_file_id>/', views.generate_notes, name='generate_notes'),
]
