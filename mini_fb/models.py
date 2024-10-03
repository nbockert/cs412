## Create a Model 
#
# mini_fb/models.py
# Define the data objects for our application
#
from django.db import models
class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''
    # data attributes of a Profile:
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_img_url = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.title} by {self.author}'