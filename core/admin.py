from django.contrib import admin
from django import forms
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import MenuItem

class MenuItemAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget = CKEditor5Widget(
            config_name="extends",
            attrs={"class": "django_ckeditor_5"}
        )

    class Meta:
        model = MenuItem
        fields = "__all__"

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemAdminForm
    list_display = ('title', 'parent', 'is_main', 'order', 'is_active', 'link_type')
    list_editable = ('order', 'is_active')
    list_filter = ('is_main', 'is_active', 'parent')
    search_fields = ('title', 'url', 'content')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ("Основные настройки", {
            'fields': ('title', 'slug', 'parent', 'order', 'is_active')
        }),
        ("Тип пункта меню", {
            'fields': ('is_main', 'is_content_page')
        }),
        ("Ссылка и контент", {
            'fields': (
                'internal_link',
                'custom_slug',
                'url',
                'content'
            ),
            'description': """
                <b>Выберите один из вариантов:</b><br>
                1. Для стандартных страниц - выберите из списка Internal link:<br>
                2. Для произвольных страниц - укажите slug<br>
                3. Для внешних ссылок - заполните URL и отключите "Страница 
                с контентом"(Is content page)<br>
                4. Для контентных страниц - заполните поле контента (Content:)
            """
        })
    )
    
    def link_type(self, obj):
        if obj.url and not obj.is_content_page:
            return "Внешняя ссылка"
        if obj.internal_link:
            return "Стандартная страница"
        if obj.custom_slug:
            return "Произвольная страница"
        return "Контентная страница"
    link_type.short_description = "Тип ссылки"