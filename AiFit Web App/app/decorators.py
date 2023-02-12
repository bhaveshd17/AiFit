from django.shortcuts import redirect,HttpResponse


def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home__page')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper_function

 
def allowed_users(allowed_roles=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            group_list = []
            if request.user.groups.exists():
                group_list = [i.name for i in request.user.groups.all() if i.name in allowed_roles]
            if len(group_list) == 0:
                return HttpResponse('You are not authorized to view this page')
            else:
                return view_function(request, *args, **kwargs)

        return wrapper_function
    return decorator
