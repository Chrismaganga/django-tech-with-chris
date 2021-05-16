from django import forms

class CreateNewList(forms.Form):
  name = forms.CharField(label="List Name", max_length=200, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter to submit..."}))