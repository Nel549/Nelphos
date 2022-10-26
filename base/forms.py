from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(
                              attrs={
                                'class': "username-1 roboto-normal-mountain-mist-16px",
                                'placeholder': 'Username'
                                }))
    email = forms.EmailField(widget=forms.EmailInput(
                              attrs={
                                'class': "username-1 roboto-normal-mountain-mist-16px",
                                'placeholder': 'Email'
                                }))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(
                              attrs={
                                'class': "username-1 roboto-normal-mountain-mist-16px",
                                'placeholder': 'First name'
                                }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(
                              attrs={'class': "username-1 roboto-normal-mountain-mist-16px",
                              'placeholder': 'Last name'
                              }))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': "username-1 roboto-normal-mountain-mist-16px",
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': "username-1 roboto-normal-mountain-mist-16px",
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ContanctForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(
                              attrs={'class': "type-your nunito-regular-normal-abbey-16px"}))
    email = forms.EmailField(widget=forms.TextInput(
                              attrs={'class': "type-your nunito-regular-normal-abbey-16px"}))
    message = forms.CharField(widget=forms.Textarea(
                              attrs={'class': "type-your-message nunito-regular-normal-abbey-16px"}))