## Create app-specific URL:
# blog/urls.py
from . import views
from django.urls import path
from .views import ShowAllView # our view class definition  
from .views import RandomArticleView
from .views import ArticleView
from django.contrib.auth import views as auth_views ##module gives generic views for login and log out and shit
urlpatterns = [
    # map the URL (empty string) to the view
    path(r'show_all', views.ShowAllView.as_view(), name='show_all'), # generic class-based view
    path(r'',views.RandomArticleView.as_view(), name='random'),
    path(r'article/<int:pk>', views.ArticleView.as_view(), name='article'), #pk is short for primary key 1. detail view (shows one record) default way is to use primary key 
    # path(r'create_comment',views.CreateCommentView.as_view(),name="create_comment"),
    path(r'article/<int:pk/create_comment',views.CreateCommentView.as_view(),name="create_comment"),
    path(r'create_article',views.CreateArticleView,name='create_article'),
    path('login/',auth_views.Login.as_view(template_name='blog/login.html'),name='login'), #put template view here - create method create seprate class
    path('logout/',auth_views.LogoutView(next_page="show_all"),name='logout'),
    path('register/',views.RegistrationView.as_view(),name='register')

]