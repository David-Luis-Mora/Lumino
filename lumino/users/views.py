# from django.contrib.auth.decorators import login_required
# # from django.http import HttpResponseForbidden
# from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from .forms import ProfileForm
from .models import Profile

# Create your views here.


def user_detail(request, username):
    user = User.objects.get(username=username)
    return render(request, 'users/user_detail.html', {'user': user})


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile has been successfully saved.')
            return redirect('users:user-detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def leave(request):
    profile = request.user.profile
    if profile.role == Profile.Role.TEACHER:
        raise PermissionDenied('Los profesores no pueden abandonar la plataforma.')
    user = request.user
    user.delete()
    messages.success(request, 'Good bye! Hope to see you soon.')
    return redirect('/')
