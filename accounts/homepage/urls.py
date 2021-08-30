from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView,
    PostDeleteView, UserPostListView, ProfileListView,
    )

urlpatterns = [
    #path('', views.homepage, name='homepage-home'),
    path('', PostListView.as_view(), name='homepage-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('homepage/dashboard/', ProfileListView.as_view(), name='homepage-dashboard'),
    path('users/search_posts', views.search_posts, name='search-posts'),
]
