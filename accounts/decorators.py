from functools import wraps

from django.shortcuts import redirect
from django.contrib import messages


def permission_required(permission):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # Superuser haben alles
            if request.user.is_superuser:
                return view_func(
                    request,
                    *args,
                    **kwargs
                )


            profile = getattr(
                request.user,
                "profile",
                None
            )


            if profile and profile.has_permission(permission):

                return view_func(
                    request,
                    *args,
                    **kwargs
                )


            messages.error(
                request,
                "Keine Berechtigung für diese Aktion!"
            )


            return redirect("core:dashboard")


        return wrapper

    return decorator