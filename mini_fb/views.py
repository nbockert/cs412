#nbockert@bu.edu
#defines the views for the application 
from .models import Profiles
from django.views.generic import ListView

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all fb profiles.'''
    model = Profiles # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all.html'
    context_object_name = 'profiles' # how to find the data in the template file