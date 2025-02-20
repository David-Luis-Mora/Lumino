# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, SignupForm

def user_login(request):
    FALLBACK_REDIRECT = reverse('subjects:subject-list')

    if request.user.is_authenticated:
        return redirect(FALLBACK_REDIRECT)
    if request.method == 'POST':
        if (form := LoginForm(request.POST)).is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user := authenticate(request, username=username, password=password):
                login(request, user)
                return redirect(request.GET.get('next', FALLBACK_REDIRECT))
            else:
                form.add_error(None, 'Incorrect username or password.')
    else:
        form = LoginForm()
    return render(
        request,
        'accounts/login.html',
        dict(form=form),
    )

@login_required
def user_logout(request):
    logout(request)
    return redirect('shared:index')

def user_signup(request):
    if request.method == 'POST':
        if (form := SignupForm(request.POST)).is_valid():
            user = form.save()
            login(request, user)
            return redirect('subjects:subject-list')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', dict(form=form))