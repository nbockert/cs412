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
    template_name = 'quotes/quote.html'
    #create dictionary of context variables for the template:
    quote = [
        "Sometimes I push the door close button on people running towards the elevator. I just need my own elevator sometimes. My sanctuary.",
        "I hate when I'm on a flight and I wake up with a water bottle next to me like oh great now I gotta be responsible for this water bottle",
        "I don't use blue. I don't like it. It bugs me out. I hate it."
    ]
    images = [
        "https://media.themoviedb.org/t/p/w600_and_h900_bestv2/xMGWSdT0mcqzentuImFmVhkEgAQ.jpg",
    ]
    context = {
        "quote1": random.choice(quote), 
        "image": random.choice(images), 
    }
    #render response to this address with that template with this context data
    return render(request,template_name,context)

