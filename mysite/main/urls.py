from django.urls import path
from . import views

urlpatterns = [
  path("<int:id>", views.list_view, name="ListView"),
  path("", views.home, name="Home")
]