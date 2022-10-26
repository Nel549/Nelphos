from dataclasses import field
from fileinput import FileInput
from .models import UserProfile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm


class EditProfileInformation(forms.ModelForm):

    bio = forms.CharField(widget=forms.Textarea(
        attrs={
            'class' : 'text-2 roboto-normal-abbey-16px',
            'placeholder': 'Bio'
        }
    ))
    instagram_link = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class' : 'text roboto-normal-abbey-16px',
            'placeholder': 'Instagram link'
        }
    ))
    facebook_link = forms.CharField(required=False,widget=forms.TextInput(
        attrs={
            'class' : 'text roboto-normal-abbey-16px',
            'placeholder': 'Facebook link'
        }
    ))
    tiktok_link = forms.CharField(required=False,widget=forms.TextInput(
        attrs={
            'class' : 'text roboto-normal-abbey-16px',
            'placeholder': 'Tiktok link'
        }
    ))
    twitter_link = forms.CharField(required=False,widget=forms.TextInput(
        attrs={
            'class' : 'text roboto-normal-abbey-16px',
            'placeholder': 'Twitter link'
        }
    ))
    pinterest_link = forms.CharField(required=False,widget=forms.TextInput(
        attrs={
            'class' : 'text roboto-normal-abbey-16px',
            'placeholder': 'Pinterest link'
        }
    ))

    class Meta:
        model = UserProfile
        exclude = ['user', 'total_orders']

class EditUserData(forms.ModelForm):

    username = forms.CharField(required=False,widget=forms.TextInput(
        attrs={
            'class' : 'text roboto-normal-abbey-16px',
            'placeholder': 'Username'
        }
    ))
    email = forms.EmailField(required=False,widget=forms.EmailInput(
        attrs={
            'class' : 'text roboto-normal-abbey-16px',
            'placeholder': 'Username'
        }
    ))
    first_name = forms.CharField(required=False,widget=forms.TextInput(
        attrs={
            'class' : 'text roboto-normal-abbey-16px',
            'placeholder': 'First name'
        }
    ))
    last_name = forms.CharField(required=False,widget=forms.TextInput(
        attrs={
            'class' : 'text roboto-normal-abbey-16px',
            'placeholder': 'Last name'
        }
    ))



    class Meta:
        model = User
        fields = '__all__'
        exclude = ['password', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined']

class EditProfileImage(forms.ModelForm):
    profileImage = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class' : 'hidden_input update-profile-foto roboto-normal-black-16px',
            'id': 'file_input'
        }
    ))
    
    class Meta:
        model = UserProfile
        exclude = ['user', 'bio', 'instagram_link', 'facebook_link', 'twitter_link', 'tiktok_link','pinterest_link']

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'password-1 roboto-normal-mountain-mist-16px',
        'placeholder': 'Email',
        'type': 'email',
        'name': 'Send'
        }))

class UserNewPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.EmailField(label='', widget=forms.PasswordInput(attrs={
        'class': 'new-password-1 roboto-normal-mountain-mist-16px',
        'placeholder': 'New password',
        'type': 'password',
        'name': 'new_password1'
        }))
    new_password2 = forms.EmailField(label='', widget=forms.PasswordInput(attrs={
        'class': 'new-password-1 roboto-normal-mountain-mist-16px',
        'placeholder': 'Confirm new password',
        'type': 'password',
        'name': 'new_password2'
        }))




   