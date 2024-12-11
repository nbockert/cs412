# project/models.py
#nbockert@bu.edu
#models that define application
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import pycountry
from collections import Counter
COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in pycountry.countries]
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Account(models.Model):
    '''Data attributes of account'''
    email = models.TextField(blank=False)
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    #collect address for geolocating 
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
        '''Return the string representation of this account'''
        return f'{self.first} {self.last}'

    def get_absolute_url(self):
        '''Return the URL to access a particular account instance.'''
        return reverse('show_account', kwargs={'pk': self.pk})
    def get_images(self):
        """"Returns Account image"""
        image_file = Account_Image.objects.filter(account=self)
        return image_file
    def get_trips(self):
        """Returns the trips taken by the user"""
        trips = Trip.objects.filter(account=self)
        return trips
    def get_friends(self):
        '''Return a list of accounts that are friends with this account.'''
        # Get friends where this account is account1
        friends_as_account1 = Friend.objects.filter(account1=self).values_list('account2', flat=True)
        # Get friends where this account is account2
        friends_as_account2 = Friend.objects.filter(account2=self).values_list('account1', flat=True)
        # Combine both sets of friends into a single list
        all_friend_ids = list(friends_as_account1) + list(friends_as_account2)
        # Retrieve account instances for all these IDs
        friends_accounts = Account.objects.filter(id__in=all_friend_ids)
        # Convert the QuerySet to a list and return
        return list(friends_accounts)
    
    def get_full_address(self):
        """Returns the full address of the user."""
        return f"{self.street_address}, {self.city}, {self.country}"
    
    def add_friend(self, other):
        # Check if 'other' is not the same as 'self'
        if self == other:
            return  # Do nothing if attempting to add self as a friend
        # Check if a Friend relationship already exists (in either direction)
        exists_as_account1 = Friend.objects.filter(account1=self, account2=other).exists()
        exists_as_account2 = Friend.objects.filter(account1=other, account2=self).exists()
        # If no relationship exists, create a new Friend instance
        if not (exists_as_account1 or exists_as_account2):
            Friend.objects.create(account1=self, account2=other)
    
    def get_friend_suggestions(self):
        '''Return a list of accounts that are not friends with this account and do not include this account.'''
        # Get all accounts excluding the current account
        all_accounts = Account.objects.exclude(id=self.id)
        
        # Get accounts that are already friends with this account
        friends_accounts = self.get_friends()
        # Exclude already-friends accounts from all_accounts to get suggestions
        suggestions = all_accounts.exclude(id__in=[friend.id for friend in friends_accounts])
        print(suggestions)
        return suggestions
    def get_trip_feed(self):
        '''Return a QuerySet of Trips from this account and all friends, ordered by recency.'''
        # Get this account's ID and all friend IDs.
        account_ids = [self.id] + [friend.id for friend in self.get_friends()]
        # Retrieve status messages for this account and all friends.
        trips = Trip.objects.filter(account__id__in=account_ids).order_by('-timestamp')
        return trips
    def get_plans(self):
        plans = Planner.objects.filter(account=self)
        return plans
    def get_score(self):
        score = Score.objects.get(account=self)
        return score







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
    def get_comments(self):
        '''Return a QuerySet of all Comments on this Trip.'''

        # use the ORM to retrieve Comments for which the FK is this Article
        comments = Comment.objects.filter(trip=self)
        return comments




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
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    maptiler_api_key = models.CharField(max_length=255, blank=True)
    geoapify_api_key = models.CharField(max_length=255, blank=True)
 
    def __str__(self):
        return f"{self.account}'s plan for {self.planner_city}"
    def add_planner_collaborators(self,other):
        """
        Adds a collaborator to this planner.
        """
        Collaborators_Plan.objects.create(planner=self, collaborator=other)
        return
    def category_counts(self):
        pois = self.get_poi()
        categories = [poi.category for poi in pois]
        return dict(Counter(categories))

    def get_poi(self):
        # Returns the places of intrest for this planner
        poi = POI.objects.filter(planner=self)
        return poi
        

    
class Friend(models.Model):
    account1=models.ForeignKey('Account',on_delete=models.CASCADE,related_name="account1")
    account2=models.ForeignKey('Account',on_delete=models.CASCADE,related_name="account2")
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.account1} & {self.account2}"

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
    
class Score(models.Model):
    account = models.ForeignKey("Account",on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)

    def get_friends(self):
        """Retrieve the account's friends."""
        friends = self.account.get_friends()
        return friends
    def get_score(self):
        """Updates the number of trips and calculates the travel score."""
        # Update the number of trips using get_trips method
        trips = Trip.objects.filter(account=self.account)

        # Calculate the score based on distances
        total_distance = 0.0
        geolocator = Nominatim(user_agent="travel_app")

        # Get home location coordinates
        full_address = self.account.get_full_address()
        if not full_address:
            print("No address available")
            home_coords = None
        else:
            try:
                home_location = geolocator.geocode(full_address)
                if home_location:
                    home_coords = (home_location.latitude, home_location.longitude)
                else:
                    print("Address not found.")
                    home_coords = None
            except Exception as e:
                print(f"Geocoding failed: {e}")
                home_coords = None

        if home_coords:
            for trip in trips:
                try:
                    trip_location = geolocator.geocode(trip.get_full_trip())
                    trip_coords = (trip_location.latitude, trip_location.longitude)
                    distance = geodesic(home_coords, trip_coords).miles
                    total_distance += distance
                except:
                    print("was not able to geocode trips")
                    pass  # Skip any trips that fail to geolocate

            # Example scoring: divide total distance by number of trips
            self.score = round(total_distance, 2)  
        else:
            self.score = 0  # Set score to 0 if home coordinates are unavailable

        # Save changes
        self.save() 
    def __str__(self):
        return f"{self.account}'s score {self.score}"

class POI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    planner = models.ForeignKey("Planner",on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('accommodation', 'Accommodation'),
        ('airport', 'Airport'),
        ('commercial', 'Commercial'),
        ('catering', 'Catering'),
        ('entertainment', 'Entertainment'),
        ('natural', 'Natural'),
        ('rental', 'Rental'),
        ('tourism', 'Tourism'),
        ('adult', 'Adult'),
        ('production', 'Production')
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    place_name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return self.place_name
