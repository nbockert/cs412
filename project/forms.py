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