# doubt_solver/urls.py
from django.urls import path
from . import views

app_name = "doubt_solver"

urlpatterns = [
    path('', views.doubt_solver, name='doubt_solver'),
]