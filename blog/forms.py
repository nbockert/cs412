# blog/forms.py
from django import forms 
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    '''A form to add a comment to an article to the database'''
    class Meta:
        '''info about class def -specify which model you want to create model for'''
        model = Comment 
        '''must create fields attribute - which fields to include in the form'''
        # fields=['article','author','text']
        fields = ['author','text']

