from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from HRMS.models import Employee

class UserRegisterForm(UserCreationForm):
    pass
    # class Meta:
    #     model = User
    #     fields = ['username', 'password1', 'password2']