## Create app-specific URL:
# mini_fb/urls.py
#nbockert@bu.edu
#routes URLS to the show all view 
from django.urls import path
from .views import ShowAllProfilesView # our view class definition 
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), # generic class-based view
]