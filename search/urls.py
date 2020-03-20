from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path("", views.index, name="search_api"),
]
