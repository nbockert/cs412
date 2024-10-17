## Create app-specific URL:
# blog/urls.py
from . import views
from django.urls import path
from .views import ShowAllView # our view class definition  
from .views import RandomArticleView
from .views import ArticleView
urlpatterns = [
    # map the URL (empty string) to the view
    path(r'show_all', views.ShowAllView.as_view(), name='show_all'), # generic class-based view
    path(r'',views.RandomArticleView.as_view(), name='random'),
    path(r'article/<int:pk>', views.ArticleView.as_view(), name='article'), #pk is short for primary key 1. detail view (shows one record) default way is to use primary key 
    # path(r'create_comment',views.CreateCommentView.as_view(),name="create_comment"),
    path(r'article/<int:pk/create_comment',views.CreateCommentView.as_view(),name="create_comment"),
    path(r'create_article',views.CreateArticleView,name='create_article'),
]