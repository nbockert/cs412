## formdata/views.py 
## get the form to display as "main" web page for this app:
from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
def show_form(request):
    '''Show the web page with the form.'''
    template_name = "formdata/form.html"
    #render function builds response using this template 
    return render(request, template_name)

## edit formdata/views.py: add submit function
def submit(request):
    '''Handle the form submission.
    Read the form data from the request,
    and send it back to a template
    '''
    template_name = "formdata/confirmation.html"
    # read the form data into python variables:
    print(request.POST)

    if request.POST:
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']
        context = {
            'name': name,
            'favorite_color':  favorite_color,
        }
        return render(request, template_name, context=context)

# return HttpResponse("nope")
    # template_name='formdata/form.html'
    # return render(request,template_name)
    #a better solution: redirect to the correct url 
    return redirect("show_form")
