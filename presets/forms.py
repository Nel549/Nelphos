from .models import Preset, Review, Tags
from django import forms

class UploadPresetForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
                              attrs={
                                'class': "text roboto-normal-abbey-16px",
                                'placeholder': 'Name',
                            }))
    description = forms.CharField(max_length=2000, widget=forms.Textarea(
                              attrs={
                                'class': "text-2 roboto-normal-abbey-16px",
                                'placeholder': 'Write some useful information about your preset'
                            }))
    file = forms.FileField(widget=forms.FileInput(
        attrs={
            'id': 'upload-btn'
            ''
        }
    ))
    
    cover = forms.ImageField(widget=forms.FileInput(
        attrs={
            'id': 'file_input',
            'class': 'hidden_input'
        }
    ))
    
    price = forms.CharField(widget=forms.NumberInput(
                              attrs={
                                'class': "text roboto-normal-abbey-16px",
                                'placeholder': '$$$'
                            }))
    tags = forms.CharField(max_length=200, widget=forms.TextInput(
                              attrs={
                                'class': "text roboto-normal-abbey-16px",
                                'placeholder': 'Tags splited by ,'
                            }))

    class Meta:
        model = Preset
        fields = '__all__'
        exclude = ['seller' , 'clicks', 'rateing']

class EditPresetForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
                              attrs={
                                'class': "text roboto-normal-abbey-16px",
                                'placeholder': 'Name',
                            }))
    description = forms.CharField(max_length=2000, widget=forms.Textarea(
                              attrs={
                                'class': "text-2 roboto-normal-abbey-16px",
                                'placeholder': 'Write some useful information about your preset'
                            }))
    file = forms.FileField(widget=forms.FileInput(
        attrs={
            'id': 'upload-btn'
            ''
        }
    ))
    
    cover = forms.ImageField(widget=forms.FileInput(
        attrs={
            'id': 'file_input',
            'class': 'hidden_input'
        }
    ))
    
    price = forms.CharField(widget=forms.NumberInput(
                              attrs={
                                'class': "text roboto-normal-abbey-16px",
                                'placeholder': '$$$'
                            }))
    tags = forms.CharField(max_length=200, widget=forms.TextInput(
                              attrs={
                                'class': "text roboto-normal-abbey-16px",
                                'placeholder': 'Tags splited by ,'
                            }))
    
    class Meta:
        model = Preset
        fields = '__all__'
        exclude = ['seller', 'rateing', 'clicks']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        members = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
        exclude = ['user', 'created_at', 'product', 'clicks', 'rateing']
