from django.views.generic.detail import SingleObjectMixin
from users.views import signup
from django.contrib.auth import decorators, login
from homepage.decorators import allowed_users
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, request, response
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
    )
from .models import Post
from .decorators import allowed_users
from django.utils.decorators import method_decorator
from django.db.models import Q


def homepage(request):
    user = User.objects.get(request.user)
    if not request.user.is_authenticated():
        return response.HttpResponseRedirect('login')
    else:
        return response.HttpResponseRedirect('board')

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'homepage/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'homepage/user_posts.html'
    #template_name = 'homepage/board.html'
    context_object_name = 'posts'
    #ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class ProfileListView(ListView):
    model = Post
    template_name = 'homepage/dashboard.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

#@allowed_users(allowed_roles=['Employer', 'admin'])
@method_decorator(allowed_users(allowed_roles=['Employer', 'admin']), name='dispatch')
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'location', 'department', 'function']
     
      
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
 
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'location', 'department', 'function', 'new', 'active', 'hired' ]
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def search_posts(request):
    if request.method == "POST":
        searched = request.POST['searched']
        sposts = Post.objects.filter(Q(location__contains=searched) |
        Q(function__contains=searched) | Q(department__contains=searched))
        return render(request, 'users/search_posts.html', {'searched':searched, 'sposts':sposts})
    else:
        return render(request, 'users/search_posts.html', {})

def JobFilter(request):
    if request.method=="POST":
        location=request.POST.get('location')
        department=request.POST.get('department')
        function=request.POST.get('function')
        optionsA=Post.objects.raw('select * from homepage where location="'+location+'" and department="'+department+'" and function="'+function+'"')
        return render(request, 'user_post.html',{"Post":optionsA})
    else:
        optionsB=Post.objects.raw('select * from homepage')
        return render(request, 'user_post.html',{"Post":optionsB})
