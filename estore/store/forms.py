#from django.db import models
#from django.db.models import fields
#from django.forms import widgets
#from django.forms.fields import CharField
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from store.models import Address

# Registration Form to create/register a new user into the system
class RegistrationForm(UserCreationForm):
    email = forms.CharField(label="Email Address", required=True, widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'Email Address'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {'username' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Username'})}

# Login Form
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autofocus' : True}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-control', 'autocomplete' : 'current-password'}))

# Set Password Form
class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-control', 'autocomplete' : 'new-password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label="Confirm Password", strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-control', 'autocomplete' : 'new-password'}))

# Password Reset Form (send confirmation to email)
class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class' : 'form-control', 'autocomplete' : 'email'}))

# Password Change Form (requires old password)
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-control', 'auto-focus' : True, 'autocomplete' : 'current-password', 'placeholder' : 'Current Password'}))
    new_password1 = forms.CharField(label="New Password", strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-control', 'autocomplete' : 'new-password', 'placeholder' : 'New Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label="Confirm Password", strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-control', 'autocomplete' : 'new-password', 'placeholder' : 'Confirm Password'}))

# Address Form
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['location', 'street_address', 'city', 'state']
        widgets = {
            'location' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Location Name'}),
            'street_address' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Street Address'}),
            'city' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'city'}),
            'state' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'state'}),
        }