from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import ImageField
from PIL import Image
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom manager to handle user creation.
    We need this because we removed the 'username' field, so the default
    Django manager (which expects a username) would crash.
    """

    def create_user(self, email, password=None, **extra_fields):
        # 1. Check if the email was provided. If not, stop everything and show an error.
        if not email:
            raise ValueError('The Email field must be set')
        
        # 2. Convert the email domain to lowercase (e.g., Jason@GMAIL.com -> Jason@gmail.com)
        # This ensures we don't have duplicate accounts just because of capitalization.
        email = self.normalize_email(email)
        
        # 3. Create a new user object in memory (not saved to database yet).
        # We pass the cleaned email and any extra info (like first_name, last_name).
        user = self.model(email=email, **extra_fields)
        
        # 4. Handle the password securely.
        # This takes the plain text password ("secret123") and scrambles it 
        # into a secure hash so it can't be read by hackers.
        user.set_password(password)
        
        # 5. Save the user to the actual database.
        # 'using=self._db' ensures it saves to the correct database if you have multiple.
        user.save(using=self._db)
        
        # 6. Return the finished user object so the code that called this function can use it.
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        This runs when you create an Admin account (e.g., via 'python manage.py createsuperuser').
        It sets special permissions and then reuses the create_user logic above.
        """
        
        # 1. Add 'is_staff=True' to the extra_fields dictionary.
        # This allows the user to log into the Django Admin panel.
        extra_fields.setdefault('is_staff', True)
        
        # 2. Add 'is_superuser=True' to the extra_fields dictionary.
        # This gives the user full permission to do anything (delete users, edit data).
        extra_fields.setdefault('is_superuser', True)
        
        # 3. Call the 'create_user' function defined above to actually build and save the user.
        # We pass the email, password, and the extra_fields (which now include the admin flags).
        return self.create_user(email, password, **extra_fields)

class Organization(models.Model):
    name = models.CharField(max_length=100)
    phonenumber = PhoneNumberField(blank=True, region='GH')
    address = models.CharField(max_length=255, help_text="Address of the organization")
    invite_token = models.UUIDField(unique=True, default =uuid.uuid4, editable=False) #Attached to a url to add users to organizations
    
    def __str__(self):
        return self.name.title()
    


class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    phonenumber = PhoneNumberField(blank=True, region='GH')
    username = None #Remove Username from table
    USERNAME_FIELD = 'email' #Tells django to use email instead of username
    email = models.EmailField(unique=True)
    
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STAFF = 'STAFF', 'Staff'
    
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STAFF)


    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name.title() + ' ' + self.last_name.title()


class Restaurant(models.Model):
    name = models.CharField(max_length=50, help_text="What\'s the name of your Restaurant?")
    phonenumber = PhoneNumberField(blank=True, region='GH')
    restaurant_img = ImageField(upload_to='restaurant_images', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
        if self.restaurant_img:
            img = Image.open(self.restaurant_img.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300,300))
                img.save(self.restaurant_img.path)

    def __str__(self):
        return self.name.title()

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_item = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    food_image = ImageField(upload_to='food_images', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.food_image:
            img = Image.open(self.food_image.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300,300))
                img.save(self.food_image.path)

    def __str__(self):
        return f"{self.menu_item.title()} - {self.restaurant.name.title()}"
    

class UserOrderActions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True) #Time of order

    @property
    def total_price(self):
        return self.menu_item.price * self.quantity

    is_ordered = models.BooleanField(default=False) #True = Order has been placed False equals in cart

    def __str__(self):
        return f"{self.user} ordered {self.quantity} of {self.menu_item}"

    
