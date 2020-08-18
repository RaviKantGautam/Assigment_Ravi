from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_client and request.user.is_active:
            return redirect('assignment:request')
        return view_func(request, *args, **kwargs)

    return wrapper_func
