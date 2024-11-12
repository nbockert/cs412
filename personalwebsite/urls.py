
from django.urls import path ##library of urls for url functions 
from django.conf import settings ##config package that lets file know abt project level settings 
from . import views

##list element 
urlpatterns = [
    path(r'',views.home,name="home"),
    path('portfolio/',views.projects,name='projects'),
    path(r"work",views.work,name="work"),
] 
