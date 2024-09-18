##hw/views.py
## description: write view functions to handle URL requests for hw app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random 
# Create your views here.

# def home(request):
#     '''Handle the main URL for the hw app.'''
#     response_text=f'''
#     <html>
#     <h1>Hello, World!</h1>
#     <p>This is our first django web application</p>
#     <hr>
#     This page was generated at {time.ctime()}.
#     </html>'''
    
#     # create response for client

#     return HttpResponse(response_text)

def home(request):
    '''
    Function to handle the URL request for /hw (home page).
    Delegate rendering to the template hw/home.html
    '''
    template_name = 'hw/home.html'
    #create dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
        "letter1":chr(random.randint(65,90)), #a letter from a-z
        "letter2": chr(random.randint(65,90)), #a letter from a-z
        "number": random.randint(1,10),
    }
    #render response to this address with that template with this context data
    return render(request,template_name,context)

