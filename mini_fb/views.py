

# Create your views here.
from django.shortcuts import render
from django.urls import reverse
# Create your views here.
#nbockert@bu.edu
#defines the views for the application 
# from .models import Profiles, Profile
from django.views.generic import ListView, DetailView
from .models import *
from typing import Any
# from django.urls import reverse

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all fb profiles.'''
    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfilePageView(DetailView):
    '''Creates a subclass of DetailView to display a single profile'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
   


