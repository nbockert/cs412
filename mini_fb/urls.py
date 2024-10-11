## Create app-specific URL:
# mini_fb/urls.py
#nbockert@bu.edu
#routes URLS to the show all view 
from django.urls import path
from . import views
from .views import ShowAllProfilesView, ShowProfilePageView # our view class definition 
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), # generic class-based view
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),
]