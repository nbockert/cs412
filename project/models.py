from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import pycountry
COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in pycountry.countries]

# Create your models here.
#NEED TO CREATE A MODEL FOR COLLABORATORS AND RETHINK PLANNER MODEL
#planner is a type of trip - but you can have many planned trips so this is a many to many relationship 
#plan trip vs post trip - attribute when you create trip? 
#add collaborators to trip model and make an organizer so it is many to one
#Should Plan just be a view? - no plan should be its own form and it should not be related to trips it should be like trips
# Ok so then instead of itinerary you should just incorporate an api that allows you to search and click buttons in things you would be interested in and then write an accessor to get events
# with collaborators what would the attributes be? 
# many to many models need an extra model to define a relationship
class Account(models.Model):
    '''Data attributes of Profile'''
    email = models.TextField(blank=False)
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    street_address = models.TextField(blank=False)
    city = models.TextField(blank=False)
    country = models.CharField(
        max_length=2,  # Use ISO 3166-1 alpha-2 country codes
        choices=COUNTRY_CHOICES,
        default="US",  # Default to United States
    )

    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # image_file = models.ImageField(blank=True)
    def __str__(self):
        '''Return the string representation of this profile'''
        return f'{self.first} {self.last}'
    def get_absolute_url(self):
        '''Return the URL to access a particular profile instance.'''
        return reverse('show_account', kwargs={'pk': self.pk})
    def get_images(self):
        """"Returns Account image"""
        image_file = Account_Image.objects.filter(account=self)
        return image_file
    def get_trips(self):
        """Returns the trips taken by the user"""
        trips = Trip.objects.filter(account=self)
        return trips
    def get_score(self):
        """Retrieves the user's travel score"""
        score = Score.objects.filter(account=self)
        return score
    def get_friends(self):
        '''Return a list of profiles that are friends with this profile.'''
        # Get friends where this profile is profile1
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        # Get friends where this profile is profile2
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        # Combine both sets of friends into a single list
        all_friend_ids = list(friends_as_profile1) + list(friends_as_profile2)
        # Retrieve Profile instances for all these IDs
        friends_profiles = Account.objects.filter(id__in=all_friend_ids)
        # Convert the QuerySet to a list and return
        return list(friends_profiles)
    
    def get_full_address(self):
        """Returns the full address of the user."""
        return f"{self.address_street}, {self.city}, {self.country}"
    
    def add_friend(self, other):
        # Check if 'other' is not the same as 'self'
        if self == other:
            return  # Do nothing if attempting to add self as a friend
        # Check if a Friend relationship already exists (in either direction)
        exists_as_profile1 = Friend.objects.filter(profile1=self, profile2=other).exists()
        exists_as_profile2 = Friend.objects.filter(profile1=other, profile2=self).exists()
        # If no relationship exists, create a new Friend instance
        if not (exists_as_profile1 or exists_as_profile2):
            Friend.objects.create(profile1=self, profile2=other)
    
    def get_friend_suggestions(self):
        '''Return a list of profiles that are not friends with this profile and do not include this profile.'''
        # Get all profiles excluding the current profile
        all_profiles = Account.objects.exclude(id=self.id)
        # Get profiles that are already friends with this profile
        friends_profiles = self.get_friends()
        # Exclude already-friends profiles from all_profiles to get suggestions
        suggestions = all_profiles.exclude(id__in=[friend.id for friend in friends_profiles])
        return suggestions
    def get_news_feed(self):
        '''Return a QuerySet of status messages from this profile and all friends, ordered by recency.'''
        # Get this profile's ID and all friend IDs.
        profile_ids = [self.id] + [friend.id for friend in self.get_friends()]
        # Retrieve status messages for this profile and all friends.
        trips = Trip.objects.filter(profile__id__in=profile_ids).order_by('-timestamp')
        return trips

class Trip(models.Model):
    '''Data attributes of status messages'''
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    trip_city = models.CharField(max_length=255)
    trip_country = models.CharField(
        max_length=2,  # Use ISO 3166-1 alpha-2 country codes
        choices=COUNTRY_CHOICES,
        default="US",  # Default to United States
    )
    
    timestamp = models.DateTimeField(auto_now=True)
    date_start = models.DateField()
    date_end = models.DateField()
    message = models.TextField()
    def __str__(self):
        return f" {self.trip_city},{self.trip_country}"
    def get_images(self):
        image_file = Trip_Image.objects.filter(trip=self)
        return image_file
    def add_trip_collaborators(self,other):
        """
        Add a collaborator to this trip
        """
        Collaborators_Trip.objects.create(trip=self, collaborator=other)
    def get_full_trip(self):
        """Returns the full trip of the user."""
        return f"{self.trip_city}, {self.trip_country}"

class Score(models.Model):
    account = models.ForeignKey("Account",on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    
    def update_travel_data(self):
        """Updates the number of trips and calculates the travel score."""
        # Update the number of trips using get_trips method
        trips = Trip.objects.filter(account=self.account)

        # Calculate the score based on distances
        total_distance = 0.0
        geolocator = Nominatim(user_agent="travel_app")

        # Get home location coordinates
        try:
            home_location = geolocator.geocode(self.user.get_full_address())
            home_coords = (home_location.latitude, home_location.longitude)
        except:
            home_coords = None  # Handle errors if geolocation fails

        if home_coords:
            for trip in trips:
                try:
                    trip_location = geolocator.geocode(trip.get_full_trip())
                    trip_coords = (trip_location.latitude, trip_location.longitude)
                    distance = geodesic(home_coords, trip_coords).miles
                    total_distance += distance
                except:
                    pass  # Skip any trips that fail to geolocate

            # Example scoring: divide total distance by number of trips
            self.score = total_distance
        else:
            self.score = 0  # Set score to 0 if home coordinates are unavailable

        # Save changes
        self.save() 
    def __str__(self):
        return f"{self.account}'s score: {self.score}"
class Trip_Image(models.Model):
    image_file = models.ImageField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE, null=True, blank=True, related_name='trip_images')
class Account_Image(models.Model):
    image_file = models.ImageField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey("Account", on_delete=models.CASCADE, null=True, blank=True, related_name='account_images')
    def __str__(self):
        return f"{self.account}: {self.image_file}"
class Planner(models.Model):
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    planner_city = models.CharField(max_length=255)
    planner_country = models.CharField(
        max_length=2,  # Use ISO 3166-1 alpha-2 country codes
        choices=COUNTRY_CHOICES,
        default="US",  # Default to United States
    )
    
    date_start = models.DateField()
    date_end = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.account}'s plan for {self.planner_city}"
    def add_planner_collaborators(self,other):
        """
        Adds a collaborator to this planner.
        """
        Collaborators_Plan.objects.create(planner=self, collaborator=other)
        return

    def calculate_trip_cost(self):
        # Placeholder for logic to integrate an API for expense calculation
        pass

    def generate_itinerary(self):
        # Placeholder for logic to interact with an itinerary API
        pass

    
class Friend(models.Model):
    profile1=models.ForeignKey('Account',on_delete=models.CASCADE,related_name="profile1")
    profile2=models.ForeignKey('Account',on_delete=models.CASCADE,related_name="profile2")
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.profile1} & {self.profile2}"

class Comment(models.Model):
    '''Encapsulate the idea of a comment on an article'''
    #model the 1 to many relationship with Article (foreign key)
    trip = models.ForeignKey("Trip",on_delete=models.CASCADE) #deletes even if there is comments 
    account = models.ForeignKey("Account",on_delete=models.CASCADE) 
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return the string representation of this comment'''
        return f'{self.text}'



class Collaborators_Trip(models.Model):
    collaborator = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="other")
    trip = models.ForeignKey("Trip",on_delete=models.CASCADE, related_name="trip_collaborators")
    def __str__(self):
        return f"{self.collaborator} on {self.trip.trip_city}"
    
class Collaborators_Plan(models.Model):
    collaborator = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="collabs")
    planner = models.ForeignKey("Planner",on_delete=models.CASCADE,related_name="planner_collaborators")

    def __str__(self):
        return f"{self.collaborator} on {self.planner.planner_city}"
    
