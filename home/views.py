from django.shortcuts import render
from home import forms

def index(request):
    return render(request, 'home/index.html')


def RegistrationView(request):
    form = forms.RegistrationForm