from django.shortcuts import render
# Create your views here.
#nbockert@bu.edu
#defines the views for the application 
from .models import Profiles, Profile
from django.views.generic import ListView, DetailView
from .models import *
from typing import Any

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all fb profiles.'''
    model = Profiles # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
    def get_context_data(self,**kwargs:Any):
        context = super().get_context_data(**kwargs)
        profile = Profiles.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
