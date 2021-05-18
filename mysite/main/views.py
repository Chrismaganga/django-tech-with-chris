from django.core.checks.messages import Debug
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.

def list_view(response, id):
  ls = ToDoList.objects.get(id=id)
  print("DEBUG: ", response.user.is_authenticated)
  print("DEBUG: ", response.user.id)
  if response.user.is_authenticated and ls.user.id == response.user.id:
    # If user logged in and owner of list
    if response.method == "POST":
      if response.POST.get("save"):
        for item in ls.item_set.all():
          if response.POST.get(str(item.id) + "_c") == "checked":
            item.complete = True
          else:
            item.complete = False

          item.save()

        if response.POST.get(str(item.id) + "_t"):
          for item in ls.item_set.all(): 
            item.text = response.POST.get(str(item.id) + "_t")
            item.save()

        if response.POST.get("itemDelete"):
          items_to_delete = response.POST.get("itemDelete").split(",");
          for item_id in items_to_delete:
            ls.item_set.filter(id=item_id).delete()

        if response.POST.get("listName"):
          if len(response.POST.get("listName")) > 2:
            ls.name = response.POST.get("listName")
            ls.save()


      elif response.POST.get("newItem"):
        item_text = response.POST.get("newText")
        
        if len(item_text) > 2:
          ls.item_set.create(text = item_text, complete = False)
        else:
          print("Invalid input")

      elif response.POST.get("listDelete"):
        ls.delete()
        return HttpResponseRedirect("/?error=List+deleted.")

    return render(response, "main/list.html", {"ls": ls, "response": response})

  else:
    # If user not logged in or not owner of list
    return HttpResponseRedirect("/login?error=Unauthorized+access.")

def view(response):
  if response.user.is_authenticated:
    if response.method == "POST":
      form = CreateNewList(response.POST)

      if form.is_valid():
        n = form.cleaned_data["name"]
        t = ToDoList(name = n)
        t.save()
        response.user.todolist.add(t) # models.py ToDoList.User[ForeignKey][name="todolist"]

        return HttpResponseRedirect("/view/{}".format(t.id))
      else:
        return HttpResponseRedirect("/?error=Validation+Error.")

    else:
      form = CreateNewList()
      return render(response, "main/view.html", {"form": form, "response": response})
  else:
    return HttpResponseRedirect("/login?error=Please+log+in+first.")