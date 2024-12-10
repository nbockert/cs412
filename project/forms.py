from django import forms
from .models import *

class CreateAccountForm(forms.ModelForm):
    '''A form to add a Profile to the database'''
    class Meta:
        model = Account
        fields = [ 'email','first', 'last', 'street_address','city', 'country']

class AddCollaboratorForm(forms.Form):
    collaborator_email = forms.EmailField()

class CreateTripForm(forms.ModelForm):
    '''A form to add a Trip to the database'''

    class Meta:
        '''Associate this HTML form with the Trip data model'''
        model = Trip
        fields = ['trip_city','trip_country','date_start','date_end','message'] # which fields to include in the form]

class UpdateAccountForm(forms.ModelForm):
        '''A form to update an account'''
        class Meta:
            '''Associate this HTML form with the Account data model'''
            model = Account
            fields = ['email','street_address','city','country'] # can't change your name

class UpdateTripForm(forms.ModelForm):
        '''A form to update a status'''
        class Meta:
            '''Associate this HTML form with the Account data model'''
            model = Trip
            fields = ['trip_city','trip_country','date_start','date_end','message']

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment on an Trip to the database'''

    class Meta:
        '''Associate this HTML form with the Comment data model'''
        model = Comment
        fields = ['text'] # which fields to include in the form]

class PlannerForm(forms.ModelForm):

    class Meta:
        model = Planner
        fields = ['planner_city', 'planner_country', 'date_start', 'date_end', 'budget']

