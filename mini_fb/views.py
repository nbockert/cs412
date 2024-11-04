

# Create your views here.
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.
#nbockert@bu.edu
#defines the views for the application 
# from .models import Profiles, Profile
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView, View
from .models import *
from .forms import *
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

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
    def get_context_data(self, **kwargs: Any):
        '''Adds the profile object to the context data.'''
        context = super().get_context_data(**kwargs)
        user_creation_form = UserCreationForm()
        # Add the form instance to the context
        context['user_creation_form'] = user_creation_form
        return context
    def form_valid(self, form):
        # Reconstruct the UserCreationForm with POST data
        user_creation_form = UserCreationForm(self.request.POST)
        
        # Check if the UserCreationForm is valid
        if user_creation_form.is_valid():
            # Save the user and get the User instance
            user = user_creation_form.save()
            
            # Attach the new user to the Profile instance
            form.instance.user = user
            
            # Delegate the rest to the superclass method
            return super().form_valid(form)
        
        # If the user creation form is not valid, redirect back to the form with errors
        return self.form_invalid(form)


class CreateStatusMessageView(LoginRequiredMixin,CreateView):
    '''Create a subclass of CreateView to handle profile creation.'''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
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
   

class UpdateProfileView(LoginRequiredMixin,UpdateView):
    model=Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_success_url(self):
        '''Redirect to the profile page after successfully updating profile.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    def dispatch(self, request):
        '''add this method to show/debug logged in user'''
        print(f"Logged in user: request.user={request.user}")
        print(f"Logged in user: request.user.is_authenticated={request.user.is_authenticated}")
        return super().dispatch(request)

class DeleteStatusMessageView(LoginRequiredMixin,DeleteView):
    '''View to delete status messages'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name= 'delete'
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_success_url(self):
        '''Redirect to the profile page after successfully deleting a StatusMessage.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateStatusMessageView(LoginRequiredMixin,UpdateView):
    '''View to update status messages'''
    model = StatusMessage
    template_name = 'mini_fb/update_status_form.html'
    context_object_name= 'update'
    form_class = UpdateStatusForm
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    def get_success_url(self):
        '''Redirect to the profile page after successfully updating a StatusMessage.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class  CreateFriendView(View):
    '''View to handle adding a friend relationship between two profiles.'''


    def dispatch(self, request, *args, **kwargs):
        # Retrieve profile IDs from URL parameters
        profile_id = self.kwargs.get('pk')
        friend_id = self.kwargs.get('other_pk')
        profile = Profile.objects.get(pk=profile_id)
        friend_profile = Profile.objects.get(pk=friend_id)



        # Call the add_friend method on the profile
        profile.add_friend(friend_profile)

        # Redirect back to the profile page of the original profile
        return redirect('show_profile', pk=profile_id)

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        # Get the default context data from the superclass
        context = super().get_context_data(**kwargs)
        
        # Get the profile object
        profile = self.get_object()
        
        # Get friend suggestions using the method from the Profile model
        friend_suggestions = profile.get_friend_suggestions()
        
        # Add friend suggestions to the context
        context['friend_suggestions'] = friend_suggestions
        
        return context
class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    # context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''Add the news feed to the context.'''
        context = super().get_context_data(**kwargs)
        news_feed = self.object.get_news_feed()
        news_feed_with_images = [
            {
                'status': status,
                'images': status.get_images()
            } 
            for status in news_feed
        ]
        context['news_feed'] = news_feed_with_images
        return context