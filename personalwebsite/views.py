from django.shortcuts import render

# Create your views here.
##hw/views.py
## description: write view functions to handle URL requests for hw app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random 
# Create your views here.

def home(request):
    '''
    Function to handle the URL request for /hw (home page).
    Delegate rendering to the template hw/home.html
    '''
    template_name = 'personalwebsite/index.html'

    return render(request,template_name)

def projects(request):
    template_name = 'personalwebsite/projects.html'
    #render response to this address with that template with this context data
    return render(request,template_name)

def work(request):
    template_name = 'personalwebsite/work.html'
    #render response to this address with that template with this context data
    return render(request,template_name)


