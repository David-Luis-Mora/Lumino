from functools import wraps

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # raise PermissionDenied()
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')
            if request.user.profile.role != role:
                raise PermissionDenied()
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
