from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import MenuItem
from django.views.decorators.http import require_GET
import os
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "DEVELOPMENT")


def index(request):
    """Главная страница с меню"""
    main_menu = (
        MenuItem.objects.filter(is_main=True, parent__isnull=True, is_active=True)
        .order_by("order")
        .prefetch_related("children")
    )

    if ENVIRONMENT == "DEVELOPMENT":
        # Проверка данных (можно удалить после отладки)
        print("ДЛЯ ОТЛАДКИ! Пункты меню:", [item.title for item in main_menu])
        for item in main_menu:
            if item.children.exists():
                print(
                    f"ДЛЯ ОТЛАДКИ! МЕНЮ- {item.title} -имеет подменю:",
                    [child.title for child in item.children.all()],
                )
        return render(request, "core/index.html", {"main_menu": main_menu})


@require_GET
def submenu_items(request, parent_id):
    items = MenuItem.objects.filter(parent_id=parent_id, is_active=True).order_by(
        "order"
    )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        data = {
            "items": [
                {
                    "id": item.id,
                    "title": item.title,
                    "url": item.get_absolute_url(),
                    "has_children": item.has_children,
                }
                for item in items
            ]
        }
        return JsonResponse(data)

    return render(request, "core/includes/submenu_items.html", {"items": items})


def menu_content(request, pk):
    item = get_object_or_404(MenuItem, pk=pk, is_active=True)
    return render(
        request, "core/menu_content.html", {"item": item, "content": item.content}
    )


def page_detail(request, slug):
    item = get_object_or_404(MenuItem, custom_slug=slug)
    return render(
        request, "core/menu_page.html", {"item": item, "content": item.content}
    )


def page_detail_view(request, slug):
    # Получаем пункт меню по custom_slug или slug
    menu_item = get_object_or_404(
        MenuItem.objects.filter(is_active=True),
        models.Q(custom_slug=slug) | models.Q(slug=slug),
    )

    # Проверяем, является ли это страницей контента
    if not menu_item.is_content_page:
        return render(request, "menu/redirect.html", {"menu_item": menu_item})

    context = {
        "menu_item": menu_item,
        "page_title": menu_item.title,
    }
    return render(request, "menu/page_detail.html", context)


def submenu_items(request, parent_id):
    items = MenuItem.objects.filter(parent_id=parent_id, is_active=True).order_by(
        "order"
    )

    return render(request, "core/includes/submenu_items.html", {"items": items})
