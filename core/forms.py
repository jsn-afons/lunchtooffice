from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import User, Organization

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))


class SignupForm(forms.Form):
    pass

class OrganizationSignUpForm(forms.Form):
    org_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Organization Name', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))
    org_phonenumber = PhoneNumberField(region='GH', widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))
    org_address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Head Office Address', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))

    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            # FIX: Add the error specifically to the confirm_password field
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email.lower()).exists():
            raise ValidationError('User already exists')
        return email.lower()
        
    def clean_org_name(self):
        org_name = self.cleaned_data.get('org_name')
        if org_name and Organization.objects.filter(org_name=org_name).exists():
            raise ValidationError('Organization already exists')
        return org_name





