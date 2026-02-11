from django.shortcuts import render, redirect
import datetime
from .forms import *

# Create your views here.
def home(request):
    date = datetime.date.today()
    context = {
        'date':date
    }
    return render(request, 'core/index.html', context)

def login(request):
    return render(request, 'core/login.html')

def signup(request):
    return render(request, 'core/signup.html')

def restaurant_selection(request):
    return render(request, 'core/restaurant_selection.html')

def menu(request):
    return render(request, 'core/menu.html')

def logout(request):
    return redirect('home')