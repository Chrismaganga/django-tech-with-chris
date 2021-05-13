from django import forms
from django import forms

class CreateNewList(forms.Form):
  name = forms.CharField(label="List Name", max_length=200)