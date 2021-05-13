from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.

def list_view(response, id):
  ls = ToDoList.objects.get(id=id)
  return render(response, "main/list.html", {"ls": ls})

def home(response):
  return render(response, "main/home.html", {})

def create(response):
  if response.method == "POST":
    form = CreateNewList(response.POST)

    if form.is_valid():
      n = form.cleaned_data["name"]
      t = ToDoList(name = n)
      t.save()

      return HttpResponseRedirect("/{}".format(t.id))

  else:
    form = CreateNewList()
  
  return render(response, "main/create.html", {"form": form})