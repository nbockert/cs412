## Create View
# blog/views.py
# Define the views for the blog app:
#from django.shortcuts import render
from .models import Article
from django.views.generic import ListView, DetailView, CreateView
from .models import *
import random
from .forms import *
from django.urls import reverse
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login 
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect 
class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Article # retrieve objects of type Article from the database
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # how to find the data in the template file
    def dispatch(self,*args,**kwargs):
        '''implement this method to add some debug tracing '''
        #let the superclass version of this method do its work
        print(f"ShowallView.dispatch; self.request.user={self.request.user}")
        return super().dispatch(*args,**kwargs)

class RandomArticleView(DetailView):
    '''Display one article selected at random '''
    model = Article
    template_name = 'article.html'
    context_object_name = "article"
    #overwrites default get_object
    def get_object(self):
        #retrieve all of the articles
        all_articles = Article.objects.all()
        article= random.choice(all_articles)
        return article
    
class ArticleView(DetailView):
    '''Display one article selected at random '''
    model = Article
    template_name = 'article.html'
    context_object_name = "article"
 
class CreateCommentView(CreateView):
    '''A view to create a Comment on an article'''
    '''on GET: send back the form to display
    on POST: read/process the form, and save new Comment to the database
    '''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_context_data(self,**kwargs:Any):
        context = super().get_context_data(**kwargs)
        article = Article.objects.get(pk=self.kwargs['pk'])
        context['article'] = article
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success'''
        # return 'show_all' #valid url pattern
        #find the article identified by the PK from the url pattern 
        article = Article.objects.get(pk=self.kwargs['pk'])
        # return reverse('article',kwargs={'pk':article.pk})
        return reverse('article',kwargs={'pk':article.pk})
    def form_valid(self,form):
        '''This method is called '''
        print(f'CreateCommentView.form_valid() form={form.cleaned_data}')
        print(f'CreateCommentView.form.valid(): self.kwargs={self.kwargs}')
        #find the Article identified by the PK from the URL pattern 
        article = Article.objects.get(pk=self.kwargs['pk'])
        #attatch this article to the instance of the Coment to set its FK
        form.instance.article = article #like: comment.article = article
        #delegate work to superclass version of this method
        return super().form_valid(form)

#order that you pass in determines who has priority inheritance 
class CreateArticleView(LoginRequiredMixin,CreateView):
    '''A class to create a new Article Instance'''
    form=CreateArticleForm
    template_name='blog/create_article_form.html'
    def get_login_url(self):
        '''return url of login page'''
        return reverse('login')
    def form_valid(self,form):
        '''This method is called as part of the form processing.'''
        print(f'CreateArticleView.form_valid():form.cleaned_data={form.cleaned_data}')
        #find the user who is logged in 
        user = self.request.user
        #attatch that user as a FK to the new Article instance
        form.instance.user = user 
        #let the superclass do the work 
        return super().form_valid(form)
class RegistrationView(CreateView):
    '''handel of registration for new users'''
    template_name='blog/registration.html'
    form_class = UserCreationForm #built-in from django package 
    def dispatch(self,request:HttpRequest,*args:Any,**kwargs:Any)->HttpResponse:
        if self.request.POST:
            print(f"RegistrationView.dispatch: self.request.POST={self.request.POST}")
            #reconstruct the UserCreateForm from the POST data
            form = UserCreationForm(self.request.POST)
            #save the form which creates a new user 
            if not form.is_valid():
                print(f"form.errors={form.errors}")
                return super().dispatch(request,*args,**kwargs)
            user = form.save() #will commit the insert to database 
            #log in the user
            login(self.request,user)
            #note to mini_fb: attach the FK user to the Profile form instance 
            #return a response 
            return redirect(reverse('show_all'))
        #let CreateView.dispatch handle the HTTP GET request 
        return super().dispatch(request,*args,**kwargs)


