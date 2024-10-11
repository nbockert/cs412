
## Register the models with the Django Admin tool
# mini_fb/admin.py
#nbockert@bu.edu
#registers and manages models 
from django.contrib import admin
# Register your models here.
from .models import *
from .models import Profiles,Profile
admin.site.register(Profiles)
admin.site.register(Profile)