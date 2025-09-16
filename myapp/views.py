from django.shortcuts import get_object_or_404, render


def index(request):
    # type: (HttpRequest) -> HttpResponse

    """Simple view that renders a template."""
    context = {"message": "Привет, Django!"}
    return render(request, "myapp/index.html", context)
