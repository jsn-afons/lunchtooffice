from django import forms
from phonenumber_field.formfields import PhoneNumberField

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'}))


class SignupForm(forms.Form):
    ...

class OrganizationSignUpForm(forms.Form):
    org_name = forms.CharField(max_length=100)
    org_phonenumber = PhoneNumberField(region='GH')
    org_address = forms.CharField(max_length=200)

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
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data





