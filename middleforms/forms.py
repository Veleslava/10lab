from django import forms
from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponseRedirect, HttpResponse
import requests
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)

class ListForm(forms.Form):
    name = forms.CharField(label='List Name', max_length=200)

class TaskCreateForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=1000, required=False)
    completed = forms.BooleanField(required=False)
    due_date = forms.DateField(widget=SelectDateWidget())
    tags = forms.CharField(max_length=200, required=False)
    PRIORITY = (
        ('h', 'High'),
        ('m', 'Medium'),
        ('l', 'Low'),
        ('n', 'None')
    )

    priority = forms.ChoiceField(choices=PRIORITY)

class ShareForm(forms.Form):
    username = forms.CharField(max_length=100,label='Username')
    permission = forms.BooleanField(required=False,label='Edit opportunity')

class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=100, required=True)
    email = EmailField(label=_("Email address"), required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)
    
    
