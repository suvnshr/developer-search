from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="search_api"),
]
