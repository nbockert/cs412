
# Create your models here.
## Create a Model 
#
# mini_fb/models.py
# Define the data objects for our application
# nbockert@bu.edu
#stores the data for the app
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
    '''Data attributes of Profile'''
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_img_url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # image_file = models.ImageField(blank=True)
    def __str__(self):
        '''Return the string representation of this profile'''
        return f'{self.first} {self.last}'
    
    def get_status_messages(self):
        '''Return all status messages for this profile, ordered by timestamp descending.'''
        # return self.status_msg.all().order_by('-timestamp')
        status = StatusMessage.objects.filter(profile=self)
        return status
    
    def get_absolute_url(self):
        '''Return the URL to access a particular profile instance.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        '''Return a list of profiles that are friends with this profile.'''
        # Get friends where this profile is profile1
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        # Get friends where this profile is profile2
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        # Combine both sets of friends into a single list
        all_friend_ids = list(friends_as_profile1) + list(friends_as_profile2)
        # Retrieve Profile instances for all these IDs
        friends_profiles = Profile.objects.filter(id__in=all_friend_ids)
        # Convert the QuerySet to a list and return
        return list(friends_profiles)
    
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
        all_profiles = Profile.objects.exclude(id=self.id)
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
        status_messages = StatusMessage.objects.filter(profile__id__in=profile_ids).order_by('-timestamp')
        return status_messages
    


   
    
    
class StatusMessage(models.Model):
    '''Data attributes of status messages'''
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField()
    def __str__(self):
        return f"{self.message}"
    def get_images(self):
        image_file = Image.objects.filter(statusmessage=self)
        return image_file

class Image(models.Model):
    image_file = models.ImageField(blank=True)
    statusmessage = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.image_file}"


class Friend(models.Model):
    profile1=models.ForeignKey('Profile',on_delete=models.CASCADE,related_name="profile1")
    profile2=models.ForeignKey('Profile',on_delete=models.CASCADE,related_name="profile2")
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.profile1} & {self.profile2}"
    

