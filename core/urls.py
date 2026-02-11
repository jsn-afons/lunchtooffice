from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('restaurant_selection/', views.restaurant_selection, name='restaurant_selection'),
    path('menu/', views.menu, name='menu'),
    path('logout/', views.logout, name='logout'),
]