from django.urls import path
from . import views

urlpatterns = [
  path("view/<int:id>/", views.list_view, name="ListView"),
  path("", views.view, name="View"),
  path("create/", views.create, name="Create"),
]