from django.urls import path
from .views import AnketaView, success_view


app_name = 'anketa'

urlpatterns = [
    path('start/', AnketaView.as_view(), name='start'),
    path('success/', success_view, name='success'),
]