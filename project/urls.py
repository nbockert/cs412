# project/urls.py
#nbockert@bu.edu
#routes URLS to the show all view 
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    # map the URL (empty string) to the view
    path('', views.ShowAllAccountsView.as_view(), name='show_all_accounts'), # generic class-based view
    path(r'account/<int:pk>', views.ShowAccountPageView.as_view(), name='show_account'),
    path(r'create_account', views.CreateAccountView.as_view(), name='create_account'),
    path(r'trip/create_trip', views.CreateTripView.as_view(), name='create_trip'),
    path(r'account/update', views.UpdateAccountView.as_view(), name='update_account'),
    path(r'trip/<int:pk>/delete', views.DeleteTripView.as_view(), name='delete_trip'),
    path(r'trip/<int:pk>/update', views.UpdateTripView.as_view(), name='update_trip'),
    path('account/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path(r'account/add_friends/<int:other_pk>', views.CreateFriendView.as_view(), name='add_friends'),
    path('account/leaderboard/', views.LeaderboardView.as_view(), name='show_leaderboard'),
    path(r'trip/<int:pk>/create_comment', views.CreateCommentView.as_view(), name="comment"),
    path(r'trip/<int:pk>/trip_page',views.TripPage.as_view(),name='trip_page'),
    path('account/trip_feed', views.ShowTripFeedView.as_view(), name='trip_feed'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('planner/create_planner', views.CreatePlannerView.as_view(), name='create_planner'),
    path(r'planner/<int:pk>/delete', views.DeletePlannerView.as_view(), name='delete_plan'),
    path('planner/<int:pk>/map_view',views.MapView.as_view(), name='show_map'),
    path('account/my_plans',views.MyPlansView.as_view(),name='my_plans'),
    path('planner/<int:pk>/poi_search/', views.POICategoryView.as_view(), name='poi_search'),
    path('planner/<int:pk>/poi_results/', views.CreatePOIView.as_view(), name='create_poi'), 
    path('planner/<int:pk>/category_graph/', views.GraphsView.as_view(), name='graph_view'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html',), name='logout'), ## NEW
]