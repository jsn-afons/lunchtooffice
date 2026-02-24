from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_users, name='login'),
    path('signup/', views.signup, name='signup'),
    path('restaurant_selection/', views.restaurant_selection, name='restaurant_selection'),
    path('menu/<int:restaurant_id>/', views.menu, name='menu'),
    path('logout/', views.logout, name='logout'),
    path('aboutus/', views.aboutus, name='aboutus'),
]