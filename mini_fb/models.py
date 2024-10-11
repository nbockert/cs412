
# Create your models here.
## Create a Model 
#
# mini_fb/models.py
# Define the data objects for our application
# nbockert@bu.edu
#stores the data for the app
from django.db import models
class Profiles(models.Model):
    '''Encapsulate the idea of an Article by some author.'''
    # data attributes of a Profile:
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_img_url = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.first} {self.last} profile'
    def get_profile(self):
        '''Return a QuerySet of all Comments on this Article.'''

        # use the ORM to retrieve Comments for which the FK is this Article
        id = Profile.objects.filter(profile=self)
        return id
    
class Profile(models.Model):
    profile = models.ForeignKey("Profiles", on_delete=models.CASCADE)
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_img_url = models.URLField(blank=True)
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.first} {self.last} profile'
