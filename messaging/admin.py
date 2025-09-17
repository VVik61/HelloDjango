from django.contrib import admin
from .models import PrivateMessage

@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp', 'sender__role', 'recipient__role')
    search_fields = (
        'subject',
        'body',
        'sender__first_name',
        'sender__last_name',
        'recipient__first_name',
        'recipient__last_name'
    )
    readonly_fields = ('timestamp',)
    fieldsets = (
        (None, {
            'fields': ('sender', 'recipient', 'subject', 'body')
        }),
        ('Статус', {
            'fields': ('is_read', 'timestamp')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('sender', 'recipient')