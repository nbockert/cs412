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
class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Article # retrieve objects of type Article from the database
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # how to find the data in the template file

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

