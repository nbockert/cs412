from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView, View, TemplateView
from .models import *
from .forms import *
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth import login
from django.db.models import Q
from django.urls import reverse_lazy
import requests
import os
from plotly.graph_objs import Pie, Figure
from django.http import HttpResponseRedirect, JsonResponse


# Create your views here.
class ShowAllAccountsView(ListView):
    '''Create a subclass of ListView to display all accounts.'''
    model = Account # retrieve objects of type Account from the database
    template_name = 'project/show_all_accounts.html'
    context_object_name = 'accounts' # how to find the data in the template file
class ShowAccountPageView(DetailView):
    '''Creates a subclass of DetailView to display a single account'''
    model = Account
    template_name = 'project/show_account.html'
    context_object_name = 'account'
    def get_context_data(self, **kwargs):
        #pass context about user friends
        context = super().get_context_data(**kwargs)
        user_account = Account.objects.get(user=self.request.user)
        context['user_friends'] = user_account.get_friends()
        return context

#added loginrequiredmixin
class CreateAccountView(CreateView,LoginRequiredMixin):
    '''Create a subclass of CreateView to handle account creation.'''
    model = Account
    form_class = CreateAccountForm
    template_name = 'project/create_account_form.html'

    def get_login_url(self) -> str:
        return reverse('login')
    def get_context_data(self, **kwargs: Any)-> dict[str, Any]:
        '''Provide context data to the template, including both forms.'''
        context = super().get_context_data(**kwargs)
        if 'user_creation_form' not in context:
            context['user_creation_form'] = UserCreationForm()
        
        # if 'image_form' not in context:
        #     context['image_form'] = AccountImageForm() 
        return context

    def form_valid(self, form):
        '''Handle form submission and user creation.'''
        # Reconstruct UserCreationForm from POST data
        user_creation_form = UserCreationForm(self.request.POST)
        
        # Save the new User instance
        userform = user_creation_form.save()
        account = form.save(commit=False)
        
        
        account.user=userform
        form.instance.account =account
        print(account)
        account.save()
        score = Score.objects.create(account=account)
        
        #need to create a new form for uploading the images
        # image_form = AccountImageForm(self.request.POST, self.request.FILES)
        new_image = self.request.FILES.getlist('files')
        for f in new_image:
            image = Account_Image(account=account,image_file=f)
            image.save()


        # if image_form.is_valid():
        #     new_image = image_form.save(commit=False)
        #     new_image.account = account  # Attach the image to the created account
        #     new_image.save()
        login(self.request,userform)
        
        return super().form_valid(form)


    def get_success_url(self):
        '''Redirect to the profile detail page after successful creation.'''
        return reverse('show_account', kwargs={'pk': self.object.pk})
class CreateTripView(LoginRequiredMixin,CreateView):
    '''Create a subclass of CreateView to handle account creation.'''
    model = Trip
    form_class = CreateTripForm
    template_name = 'project/create_trip_form.html'
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_context_data(self, **kwargs:Any) -> dict[str, Any]:
        '''Adds the account object to the context data.'''
        context = super().get_context_data(**kwargs)
        account = Account.objects.get(user=self.request.user)
        context['account'] = account
        return context

    def form_valid(self, form):
        '''Map trip to correct account'''
        account = self.get_object()
        form.instance.account = account
        # save the trip to database
        sm = form.save(commit=False)
        sm.account = account
        sm.save()
        
        # read the file from the form:
        files = self.request.FILES.getlist('files')
        for f in files:
            image = Trip_Image(trip=sm,image_file=f)
            image.save()
        # sm.get_score()
        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to the account page after successfully posting a status message.'''
        account = Account.objects.get(user=self.request.user)
        return reverse('show_account', kwargs={'pk': account.pk})
    def get_object(self):
        # Retrieve the account based on the logged-in user
        return get_object_or_404(Account, user=self.request.user)

class UpdateAccountView(LoginRequiredMixin,UpdateView):
    model=Account
    form_class = UpdateAccountForm
    template_name = 'project/update_account_form.html'
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_success_url(self):
        '''Redirect to the profile page after successfully updating profile.'''
        return reverse('show_account', kwargs={'pk': self.object.pk})
    def dispatch(self, request):
        '''add this method to show/debug logged in user'''
        print(f"Logged in user: request.user={request.user}")
        print(f"Logged in user: request.user.is_authenticated={request.user.is_authenticated}")
        return super().dispatch(request)
    def get_object(self):
        # Retrieve the Profile based on the logged-in user
        return Account.objects.get(user=self.request.user)
    def form_valid(self, form):
        '''Override form_valid to update the score after saving the account.'''
          # Call the parent class's form_valid method
        # account = Account.objects.get(user=self.request.user)
        # form.instance.account = account
        # sm = form.save(commit=False)
        account = form.save(commit=False)
        form.instance.account = account
        account.save() 
        new_image = self.request.FILES.get('account_image')
        if new_image:
            print(new_image)
            Account_Image.objects.filter(account=account).delete()
            image = Account_Image(image_file=new_image,account=account)
            image.save()
        return super().form_valid(form)
        
   
class DeleteTripView(LoginRequiredMixin,DeleteView):
    '''View to delete trips ***NOTE HAVE TO CHANGE SCORE'''
    model = Trip
    template_name = 'project/delete_trip_form.html'
    context_object_name= 'delete'
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_success_url(self):
        '''Redirect to the profile page after successfully posting a status message.'''
        account = Account.objects.get(user=self.request.user)
        return reverse('show_account', kwargs={'pk': account.pk})
    def delete(self, request, *args, **kwargs):
        '''Override the delete method to update the account score after deletion.'''
        # First, delete the trip
        response = super().delete(request, *args, **kwargs)

        # Fetch the account associated with the logged-in user
        
        
        # Update the score after the deletion of the trip
        self.object.save()  # Save the updated account

        # Return the response to continue with the redirection
        return response

class UpdateTripView(LoginRequiredMixin,UpdateView): #NEED TO FIX
    '''View to update status messages'''
    model = Trip
    template_name = 'project/update_trip_form.html'
    context_object_name= 'update_trips'
    form_class = UpdateTripForm
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    def get_success_url(self):
        '''Redirect to the profile page after successfully posting a status message.'''
        account = Account.objects.get(user=self.request.user)
        return reverse('show_account', kwargs={'pk': account.pk})
class  CreateFriendView(View):
    '''View to handle adding a friend relationship between two accounts.'''


    def dispatch(self, request, *args, **kwargs):
        # Retrieve profile IDs from URL parameters
        friend_id = self.kwargs.get('other_pk')
        account = Account.objects.get(user=self.request.user)
        friend_profile = Account.objects.get(pk=friend_id)



        # Call the add_friend method on the profile
        account.add_friend(friend_profile)

        # Redirect back to the profile page of the original profile
        return redirect('show_account', pk=account.pk)
    def get_object(self):
        # Retrieve the Profile based on the logged-in user
        return get_object_or_404(Account, user=self.request.user)

class ShowFriendSuggestionsView(DetailView):
    model = Account
    template_name = 'project/friend_suggestions.html'

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
    def get_object(self):
        return get_object_or_404(Account, user=self.request.user)


class LeaderboardView(LoginRequiredMixin, ListView):
    model = Score
    template_name = 'project/leaderboard.html'
    context_object_name = 'leaderboard'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = Account.objects.get(user=self.request.user)
        user_score = Score.objects.get(account=account)
        user_score.get_score()

        friends = account.get_friends()
        all_scores = []
        for friend in friends:
            friend_score = Score.objects.get(account=friend)
            friend_score.get_score()
            all_scores.append(friend_score)
        all_scores.append(user_score)
        print(all_scores)
        all_scores_sorted = sorted(all_scores, key=lambda x: x.score, reverse=True)
        context['leaderboard'] = all_scores_sorted
        user_rank = all_scores_sorted.index(user_score) + 1
        context['user_rank'] = user_rank
        context['user_score'] = user_score
        return context

class CreateCommentView(LoginRequiredMixin,CreateView):
    '''
    A view to create a Comment on an Account.
    on GET: send back the form to display
    on POST: read/process the form, and save new Comment to the database
    '''

    form_class = CreateCommentForm
    template_name = "project/comment_form.html"
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def dispatch(self, request, *args, **kwargs):
        # Retrieve the Trip object using the 'trip_pk' passed in the URL
        self.trip = get_object_or_404(Trip, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        # get the context data from the sueprclass
        context =  super().get_context_data(**kwargs)
        # find the Account identified by the PK from the URL pattern
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        # add the Account referred to by the URL into this context
        context['Trip'] = trip
        context['Account'] = trip.account

        return context

    def get_success_url(self):
        '''Return the URL to redirect to on success.'''
        # Redirect to the trip page using the primary key of the trip
        return reverse('trip_page', kwargs={'pk':self.trip.pk})
       

    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''
        # Assign the trip and account to the new comment
        form.instance.trip = self.trip
        user = self.request.user
        account = Account.objects.get(user=user)
        form.instance.account = account
        return super().form_valid(form)
    
class TripPage(DetailView):
    '''
    A view to display a trip
    '''
    model = Trip
    template_name = 'project/trip_page.html'


class ShowTripFeedView(DetailView):
    model = Account
    template_name = 'project/trip_feed.html'
    # context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''Add the news feed to the context.'''
        context = super().get_context_data(**kwargs)
        trip_feed = self.object.get_trip_feed()
        trip_feed_with_images = [
            {
                'trip': trip,
                'images': trip.get_images()
            } 
            for trip in trip_feed
        ]
        context['trip_feed'] = trip_feed_with_images
        return context
    def get_object(self):
        return get_object_or_404(Account, user=self.request.user)
#fix search
class SearchView(ListView):
    template_name = 'project/search_results.html'
    context_object_name = 'results'
    model = None

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # Search for accounts by name or username
            account_results = Account.objects.filter(
                Q(name__icontains=query) | Q(user__username__icontains=query)
            )
            # Search for trips by location
            trip_results = Trip.objects.filter(
                location__icontains=query
            )
             # Combine the results into one queryset list
            context = {
                'results': {
                    'accounts': account_results,
                    'trips': trip_results,
                },
                'q': query  # Pass the query directly
            }
            return render(self.request, 'project/search_results.html', context)
            # return {
            #     'accounts': account_results,
            #     'trips': trip_results
            # }
        return {'accounts': Account.objects.none(), 'trips': Trip.objects.none()}
    

# Geoapify and Maptiler API keys (replace with your actual keys)
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
MAPTILER_API_KEY = os.getenv("MAPTILER_API_KEY")
class MapView(TemplateView):
    template_name = 'project/map_view.html'
    def get_context_data(self, **kwargs):
        # Get the planner object based on the pk from URL
        planner = get_object_or_404(Planner, pk=kwargs['pk'])

        # Return the context with the necessary data
        context = super().get_context_data(**kwargs)
        context['planner'] = planner
        context['geoapify_api_key'] = planner.geoapify_api_key
        context['latitude'] = planner.latitude
        context['longitude'] = planner.longitude
        context['planner_city'] = planner.planner_city
        context['planner_country'] = planner.planner_country
        context['maptiler_api_key'] = planner.maptiler_api_key


        return context
class CreatePlannerView(CreateView):
    """On GET: direct to planner creation form
    On POST: direct to the map view"""
    model = Planner
    form_class = PlannerForm
    template_name = 'project/create_planner.html'

    def form_valid(self, form):
        # Associate the planner with the logged-in user's account
        account = Account.objects.get(user=self.request.user)
        form.instance.account = account
    

        # Get city and country from the form data
        city = form.cleaned_data['planner_city']
        country = form.cleaned_data['planner_country']

        # Fetch coordinates using Geoapify API
        api_key = GEOAPIFY_API_KEY
        print(api_key)
        geocode_url = f"https://api.geoapify.com/v1/geocode/search?city={city}&country={country}&apiKey={api_key}"
        response = requests.get(geocode_url)

        if response.status_code == 200:
            data = response.json()
            if data['features']:
                coords = data['features'][0]['geometry']['coordinates']
                form.instance.longitude = coords[0]  # Longitude
                form.instance.latitude = coords[1]   # Latitude

        # Assign API keys to the instance
        form.instance.geoapify_api_key = api_key
        form.instance.maptiler_api_key = MAPTILER_API_KEY

        # Proceed with the default form handling (saves the instance)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_map', kwargs={'pk': self.object.pk})
    
class DeletePlannerView(LoginRequiredMixin,DeleteView):
    '''View to delete trips ***NOTE HAVE TO CHANGE SCORE'''
    model = Planner
    template_name = 'project/delete_planner_form.html'
    context_object_name= 'delete_p'
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_success_url(self):
        '''Redirect to the profile page after successfully posting a status message.'''
        return reverse('my_plans')
   
class MyPlansView(DetailView,LoginRequiredMixin):
    template_name = 'project/show_all_plans.html'
    model = Account
    def get_object(self):
        return get_object_or_404(Account, user=self.request.user)
class POICategoryView(DetailView):
    '''Upon form submission save selection by the user and display the list results'''
    model = Planner  
    template_name = 'project/poi_search.html' 
    context_object_name = 'poi_list'
    def get_context_data(self, **kwargs):
        '''Get Planner Context Data'''
        # Get the planner using the pk passed in the URL
        context = super().get_context_data(**kwargs)
        planner = get_object_or_404(Planner, pk=self.kwargs['pk'])
        context['planner'] = planner
        return context
    # def post(self, request, *args, **kwargs):
    #     category = request.POST.get('category')  # Get the category selected by the user
    #     return HttpResponseRedirect(reverse('poi_search', kwargs={'pk': self.kwargs['pk']}))


    
class CreatePOIView(CreateView):
    '''After the user selects a place from view '''
    model = POI
    template_name = 'project/show_map.html'
    context_object_name = 'poi_create'

    def get_context_data(self, **kwargs):
        '''Get Planner Context Data'''
        # Get the planner using the pk passed in the URL
        context = super().get_context_data(**kwargs)
        planner = get_object_or_404(Planner, pk=self.kwargs['pk'])
        context['planner'] = planner
        return context
    
    def post(self, request, *args, **kwargs):
        #attatch to Planner 
        planner = get_object_or_404(Planner, pk=kwargs['pk'])
        user = self.request.user
        data = request.POST
        category = data.get('category')
        place_name = data.get('place_name')
        address = data.get('address')
        longitude = data.get('longitude')
        latitude = data.get('latitude')

        # Create the POI instance
        poi = POI.objects.create(
            user=user,
            category=category,
            place_name=place_name,
            address=address,
            longitude=longitude,
            latitude=latitude,
            planner=planner
        )

        return HttpResponseRedirect(reverse('show_map', kwargs={'pk': planner.pk}))


class GraphsView(LoginRequiredMixin, ListView):
    """View to display a pie chart of a user's Places of Interest categories."""
    template_name = 'project/category_graph_view.html'
    model = Planner
    context_object_name = 'graph'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the planner object from the URL
        planner = get_object_or_404(Planner, pk=self.kwargs['pk'])
        context['planner'] = planner

        # Get category counts from the planner's `category_counts` method
        category_counts = planner.category_counts()

        # Prepare data for the pie chart
        categories = list(category_counts.keys())
        counts = list(category_counts.values())

        # Create the pie chart using Plotly
        colors = ['#16423C', '#6A9C89', '#C4DAD2', '#557C56', '#387478']
        
        pie_chart = Figure(data=[Pie(labels=categories, values=counts,marker=dict(colors=colors),textinfo='label+percent',)])
        pie_chart.update_layout(

        margin=dict(l=20, r=20, t=40, b=20),  # Adjust margins for better fit
        height=500,  # Set chart height
        font=dict(
            family="Raleway, sans-serif",
            size=14,
            color="#333"
        ),
        paper_bgcolor="#f9f9f9",  # Background color of the chart
        plot_bgcolor="#ffffff",  # Background of the plot area
    )

        # Convert the Plotly chart to HTML
        context['chart'] = pie_chart.to_html(full_html=False)

        return context
    