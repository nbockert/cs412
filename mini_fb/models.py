
# Create your models here.
## Create a Model 
#
# mini_fb/models.py
# Define the data objects for our application
# nbockert@bu.edu
#stores the data for the app
from django.db import models
from django.urls import reverse

class Profile(models.Model):
    '''Data attributes of Profile'''
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_img_url = models.URLField(blank=True)
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
   
    
    
class StatusMessage(models.Model):
    '''Data attributes of status messages'''
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField()
    def __str__(self):
        return f"{self.message}"


