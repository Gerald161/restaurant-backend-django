from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.Upload.as_view()),
]