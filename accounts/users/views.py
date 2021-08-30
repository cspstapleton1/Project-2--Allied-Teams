from django.forms.fields import ChoiceField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    )
#from homepage.views import (
#    PostListView, PostDetailView, PostCreateView, PostUpdateView,
#    PostDeleteView
#    )
from homepage.models import Post
from .forms import user_choices

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            if form.cleaned_data.get('i_am') == 'Employee':
                g = Group.objects.get(name='Employee')
                user.groups.add(g)
            if form.cleaned_data.get('i_am') == 'Employer':
                g = Group.objects.get(name='Employer')
                user.groups.add(g)


            messages.success(request, f'Your Account has been created. You are now able to log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile(request):
        context = {
            'posts': Post.objects.all()
        }   
        return render(request, 'users/profile.html', context)
