from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView, View
from .models import *
from .forms import *
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm



# Create your views here.
class ShowAllAccountsView(ListView):
    '''Create a subclass of ListView to display all fb accounts.'''
    model = Account # retrieve objects of type Article from the database
    template_name = 'project/show_all_accounts.html'
    context_object_name = 'accounts' # how to find the data in the template file
class ShowAccountPageView(DetailView):
    '''Creates a subclass of DetailView to display a single account'''
    model = Account
    template_name = 'project/show_account.html'
    context_object_name = 'account'
class CreateAccountView(CreateView):
    '''Create a subclass of CreateView to handle account creation.'''
    model = Account
    form_class = CreateAccountForm
    template_name = 'project/create_account_form.html'
    def get_context_data(self, **kwargs: Any):
        '''Adds the account object to the context data.'''
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
            
            # Attach the new user to the Account instance
            form.instance.user = user
            sm = form.save()
            # read the file from the form:
            files = self.request.FILES.getlist('files')
            for f in files:
                image = Account_Image(image_file=f,trip=sm)
                image.save()
            # Delegate the rest to the superclass method
            return super().form_valid(form)
        
        # If the user creation form is not valid, redirect back to the form with errors
        return self.form_invalid(form)

class CreateTripView(LoginRequiredMixin,CreateView):
    '''Create a subclass of CreateView to handle account creation.'''
    model = Trip
    form_class = CreateTripForm
    template_name = 'project/create_trip_form.html'
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_context_data(self, **kwargs):
        '''Adds the account object to the context data.'''
        context = super().get_context_data(**kwargs)
        account = Account.objects.get(user=self.request.user)
        context['account'] = account
        return context

    def form_valid(self, form):
        '''Map status message to correct account'''
        account = Account.objects.get(user=self.request.user)
        form.instance.account = account
        # save the status message to database
        sm = form.save()
        # read the file from the form:
        files = self.request.FILES.getlist('files')
        for f in files:
            image = Trip_Image(image_file=f,trip=sm)
            image.save()

        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to the account page after successfully posting a status message.'''
        account = account.objects.get(user=self.request.user)
        return reverse('show_account', kwargs={'pk': account.pk})
    def get_object(self):
        # Retrieve the account based on the logged-in user
        return get_object_or_404(Account, user=self.request.user)
   