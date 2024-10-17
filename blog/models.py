## Create a Model 
#this shit doesn't work because you need to create the app for blog to get the migrations
# blog/models.py
# Define the data objects for our application
#
from django.db import models
from django.urls import reverse
class Article(models.Model):
    '''Encapsulate the idea of an Article by some author.'''
    # data attributes of a Article:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.title} by {self.author}'
    
    def get_comments(self):
        '''Return a QuereySet of all Comments on this article'''
        #use the ORM to retrieve Comments for which the FK is this article
        comments = Comment.objects.filter(article=self) #match this up with foreign key 
        return comments
    def get_absolute_url(self):
        '''Return URL that will display instance of this object'''
        #self.pk is primary key to this article instance 
        return reverse('article',kwargs={'pk':self.pk})
        
class Comment(models.Model):
    '''Encapsulate the idea of a comment on an article'''
    #model the 1 to many relationship with Article (foreign key)
    article= models.ForeignKey("Article",on_delete=models.CASCADE) #deletes even if there is comments 
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return the string representation of this comment'''
        return f'{self.text}'
    
