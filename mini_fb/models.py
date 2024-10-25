
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

class Profile(models.Model):
    '''Data attributes of Profile'''
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_img_url = models.URLField(blank=True)
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
    

