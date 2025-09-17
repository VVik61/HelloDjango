from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

doctor_required = role_required('doctor', 'admin')
medical_required = role_required('medical', 'doctor', 'medsestra', 'admin')
editor_required = role_required('editor', 'admin')
patient_required = role_required('patient')