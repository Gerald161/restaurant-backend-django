from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.Upload.as_view()),
    path('search/<slug:slug>', views.Search.as_view()),
    path('remove/<slug:slug>', views.Remove.as_view()),
]