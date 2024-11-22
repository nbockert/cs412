from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(Account)
admin.site.register(Trip)
admin.site.register(Trip_Image)
admin.site.register(Account_Image)
admin.site.register(Friend)
admin.site.register(Score)
admin.site.register(Comment)
admin.site.register(Planner)
admin.site.register(Collaborators_Trip)
admin.site.register(Collaborators_Plan)