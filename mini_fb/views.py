

# Create your views here.
from django.shortcuts import render
from django.urls import reverse
# Create your views here.
#nbockert@bu.edu
#defines the views for the application 
# from .models import Profiles, Profile
from django.views.generic import ListView, DetailView, CreateView,UpdateView
from .models import *
from .forms import *
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

class CreateProfileView(CreateView):
    '''Create a subclass of CreateView to handle profile creation.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
    '''Create a subclass of CreateView to handle profile creation.'''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    def get_context_data(self, **kwargs):
        '''Adds the profile object to the context data.'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Map status message to correct profile'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        # save the status message to database
        sm = form.save()
        # read the file from the form:
        files = self.request.FILES.getlist('files')
        for f in files:
            image = Image(image_file=f,statusmessage=sm)
            image.save()

        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to the profile page after successfully posting a status message.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateProfileView(UpdateView):
    model=Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    def get_success_url(self):
        '''Redirect to the profile page after successfully updating profile.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

