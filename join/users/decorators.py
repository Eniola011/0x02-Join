from django.shortcuts import redirect
from functools import wraps

def user_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
