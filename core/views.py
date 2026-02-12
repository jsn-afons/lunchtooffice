from django.shortcuts import render, redirect
import datetime
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import transaction

# Create your views here.
def home(request):
    date = datetime.date.today()
    context = {
        'date':date
    }
    return render(request, 'core/index.html', context)

def login_users(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) #binds data from user to form

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)
            

            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back! You are now logged in.")
                return redirect('restaurant_selection')
            else:
                messages.error(request, 'Invalid email or password')
                return render(request, 'core/login.html', {'form': form})
    else: 
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'core/login.html', context)

def signup(request):
    if request.method == 'POST':
        form = OrganizationSignUpForm(request.POST) #populates with user sent data
        if form.is_valid():
            try:
                with transaction.atomic():                 
                    org = Organization.objects.create(
                        org_name = form.cleaned_data['org_name'].title(),
                        org_phonenumber = form.cleaned_data['org_phonenumber'],
                        org_address = form.cleaned_data['org_address'],
                    )
                    
                    user = User.objects.create_user(
                        first_name = form.cleaned_data['first_name'].title(),
                        last_name= form.cleaned_data['last_name'].title(),
                        email= form.cleaned_data['email'],
                        password = form.cleaned_data['password'],
                        organization= org,
                        phonenumber = form.cleaned_data['phonenumber'],
                        role= 'ADMIN'
                    )

                    login(request, user)
                    messages.success(request, f'Successfully Created {org.org_name}')
                    return redirect('restaurant_selection')

            except Exception as e:
                messages.error(request, f"An error occured: {e}")
    else:
        form = OrganizationSignUpForm()

    context = {
        'form': form
    }
    return render(request, 'core/signup.html', context)

def restaurant_selection(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, 'core/restaurant_selection.html', context)

def menu(request, restaurant_id):
    menu_items = Menu.objects.filter(restaurant=restaurant_id)
    context = {
        'menu_items': menu_items
    }
    return render(request, 'core/menu.html', context)

def logout(request):
    return redirect('home')