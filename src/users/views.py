from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserSignUpForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.

def signup_view(request):
    template_name = 'users/signup.html'
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('users-profile')
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('users-login')
    else:
        form = UserSignUpForm()
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


class LoginView(LoginView):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super(LoginView, self).dispatch(request, *args, **kwargs)
        return redirect('users-profile')


class LogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(LogoutView, self).dispatch(request, *args, **kwargs)
        return redirect('users-login')
