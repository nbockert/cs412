# projects/urls.py
#nbockert@bu.edu
#routes URLS to the show all view 
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
urlpatterns = [
    # map the URL (empty string) to the view
    path('', views.ShowAllAccountsView.as_view(), name='show_all_accounts'), # generic class-based view
    path(r'profile/<int:pk>', views.ShowAccountPageView.as_view(), name='show_account'),
    path(r'create_profile', views.CreateAccountView.as_view(), name='create_account'),
    # path(r'status/create_status', views.CreateStatusMessageView.as_view(), name='create_status'),
    # path(r'profile/update', views.UpdateProfileView.as_view(), name='update_profile'),
    # path(r'status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    # path(r'status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name='update_status'),
    # path('profile/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    # path(r'profile/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name='add_friend'),
    # path('profile/news_feed', views.ShowNewsFeedView.as_view(), name='news_feed'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html',), name='logout'), ## NEW
]