from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def signup_view(request):
    template_name = 'users/signup.html'
    form = UserCreationForm()
    context = {'form': form}
    return render(request, template_name, context)
