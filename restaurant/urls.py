## restaurant/urls.py
##description: URL patterns for the restaurant app

from django.urls import path ##library of urls for url functions 
from django.conf import settings ##config package that lets file know abt project level settings 
from . import views

##list element 
urlpatterns = [
    path(r'',views.main_func,name="main"),
    path('order/',views.orders,name='order'),
    path('confirmation/',views.submit,name="submit"),
] 
