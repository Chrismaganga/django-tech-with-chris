from django.urls import path
from . import views

urlpatterns = [
  path("<int:id>/", views.list_view, name="ListView"),
  path("", views.home, name="Home"),
  path("create/", views.create, name="Create"),
  path("view/", views.view, name="View"),
]