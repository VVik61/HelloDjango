from django.contrib import admin
from .models import Question, Anketa

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text',)

class AnketaAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'gender', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('full_name', 'answers_text')
    readonly_fields = ('created_at', 'answers_text')
    date_hierarchy = 'created_at'

admin.site.register(Question, QuestionAdmin)
admin.site.register(Anketa, AnketaAdmin)
