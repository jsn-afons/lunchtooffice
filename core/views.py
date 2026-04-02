from django.shortcuts import render, redirect
import datetime
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
            print('form submitted successfully')
            try:
                with transaction.atomic():                 
                    org = Organization.objects.create(
                        name = form.cleaned_data['org_name'].title(),
                        phonenumber = form.cleaned_data['org_phonenumber'],
                        address = form.cleaned_data['org_address'],
                    )
                    
                    user = User.objects.create_user(
                        first_name = form.cleaned_data['first_name'].title(),
                        last_name= form.cleaned_data['last_name'].title(),
                        email= form.cleaned_data['email'],
                        password = form.cleaned_data['password'],
                        organization= org,
                        phonenumber = form.cleaned_data['user_phonenumber'],
                        role= 'ADMIN'
                    )

                    login(request, user)
                    messages.success(request, f'Successfully Created {org.name}')
                    return redirect('restaurant_selection')

            except Exception as e:
                messages.error(request, f"An error occured: {e}")
    else:
        form = OrganizationSignUpForm()

    context = {
        'form': form
    }
    return render(request, 'core/signup.html', context)

@login_required
def restaurant_selection(request):
    user = request.user
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants,
        'user': user,
    }
    return render(request, 'core/restaurant_selection.html', context)

@login_required
def menu(request, restaurant_id):
    #make sure that user is tied to organization so users only see what their organization is ordering
    
    menu_items = Menu.objects.filter(restaurant=restaurant_id)
    context = {
        'menu_items': menu_items
    }
    return render(request, 'core/menu.html', context)

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        order = request.POST.get('order')
        quantity = request.POST.get('quantity')
        Order.objects.create(
            user = request.user,
            menu_item = order,
            quantity = quantity,
        )
        return redirect('menu', restaurant_id)

@login_required
def checkout_cart(request):
    with transaction.atomic():
        order = Order.objects.create(
            user = request.user,
        )
            



        

def logout(request):
    logout(request)
    return redirect('home')

def aboutus(request):
    return render(request, 'core/aboutus.html')