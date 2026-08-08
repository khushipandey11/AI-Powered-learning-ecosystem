from django.urls import path
from . import views


app_name = "file_upload"


urlpatterns = [
   path('', views.upload_file, name='upload_page'),
  #path('', views.upload_view, name='upload_home'),
  # path('test/', views.test_view, name='test_page'),
#path('generate_notes/<int:uploaded_file_id>/', views.generate_notes, name='generate_notes'),
]
