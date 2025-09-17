from django.shortcuts import redirect
from django.urls import reverse

class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            return None

        protected_paths = {
            '/medical/': ['medical', 'doctor', 'nurse', 'admin'],
            '/doctor/': ['doctor', 'admin'],
            '/editor/': ['editor', 'admin'],
            '/patient/': ['patient']
        }

        for path, allowed_roles in protected_paths.items():
            if request.path.startswith(path) and request.user.role not in allowed_roles:
                return redirect(reverse('access_denied'))