from django.contrib import admin
from .models import Organization, User, Restaurant, Menu, UserOrderAction
# Register your models here.
admin.site.register(Organization)
admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(UserOrderAction)
