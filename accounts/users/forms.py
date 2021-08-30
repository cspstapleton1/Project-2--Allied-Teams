from django import forms
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.forms import UserCreationForm
import django_filters

user_choices =(
        ('Employee', 'filling a position'),
        ('Employer', 'building a project'),
        )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=100)
    last_name = forms.CharField(min_length=2, max_length=100)
    i_am = forms.ChoiceField(choices = user_choices)
    #i_am = forms.ChoiceField(label="I am ", widget=forms.Select(choices = user_choices))
    
 #class EmployFilter(FilterSet):
    #status = ChoiceFilter(choices = user_choices)
    class Meta:
        model = User
        fields = ['username', 'email',
                  'first_name', 'last_name',
                  'i_am',
                  'password1', 'password2']
