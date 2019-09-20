from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserSignUpFor, UserUpdateForm, ProfileUpdateForm

# Create your views here.

def signup_view(request):
    template_name = 'users/signup.html'
    if request.method == 'POST':
        form = UserSignUpFor(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('users-login')
    else:
        form = UserSignUpFor()
    context = {
        'title': 'Signup',
        'form': form
    }
    return render(request, template_name, context)


@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
            instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!.')
            return redirect('users-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
