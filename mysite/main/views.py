from django.core.checks.messages import Debug
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.

def list_view(response, id):
  ls = ToDoList.objects.get(id=id)

  if response.method == "POST":
    if "save" in response.POST:
      for item in ls.item_set.all():
        if response.POST.get("c" + str(item.id)) == "checked":
          item.complete = True
        else:
          item.complete = False
        
        item.save()

    elif response.POST["newItem"]:
      item_text = response.POST.get("newText")
      
      if len(item_text) > 2:
        ls.item_set.create(text = item_text, complete = False)
      else:
        print("Invalid input")

  return render(response, "main/list.html", {"ls": ls})

def view(response):
  if response.user.is_authenticated:
    return render(response, "main/view.html", {"response": response})
  else:
    return HttpResponseRedirect("/login?error=Please+log+in+first")

def create(response):

  if response.user.is_authenticated:
    if response.method == "POST":
      form = CreateNewList(response.POST)

      if form.is_valid():
        n = form.cleaned_data["name"]
        t = ToDoList(name = n)
        t.save()
        response.user.todolist.add(t)

        return HttpResponseRedirect("/{}".format(t.id))

    else:
      form = CreateNewList()
      return render(response, "main/create.html", {"form": form})
  else:
    return HttpResponseRedirect("/login?error=Please+log+in+first")