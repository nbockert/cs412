from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database'''

    class Meta:
        '''Associate this HTML form with the Profile data model'''
        model = Profile
        # fields = ['article', 'author', 'text'] # which fields to include in the form
        fields = ['first', 'last','city','email','profile_img_url'] # which fields to include in the form]

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a Profile to the database'''

    class Meta:
        '''Associate this HTML form with the Profile data model'''
        model = StatusMessage
        fields = ['message'] # which fields to include in the form]