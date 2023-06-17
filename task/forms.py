from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from task.models import Tasks


class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    #using model form from userCreation form
    class Meta:
        model=User
        fields=["email","username","password1","password2"]
        widgets={
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form.control"}),


        }

# if we do not need create/update action then no need of ModelForm
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class TasksForm(forms.ModelForm):
    class Meta:
        model=Tasks
        fields=["task_name"]
        widget={"task_name": forms.TextInput(attrs={"class":"form-control"})}

class TasksEditForm(forms.ModelForm):
    class Meta:
        model=Tasks
        fields=["task_name","status"]
        widget={"task_name": forms.TextInput(attrs={"class":"form-control"})}
                