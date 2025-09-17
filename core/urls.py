from django.urls import path
from . import views

# app_name = 'core'

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.index, name='about'),  # Заглушка для страницы "О нас"
    path('accounts/login/', views.index, name='login'),  # Заглушка для входа
    path('anketa/', views.index, name='anketa'),  # Заглушка для анкеты
    path('contacts/', views.index, name='contacts'),  # Заглушка для контактов
    path('content/<int:pk>/', views.menu_content, name='menu-content'),
    path('pages/<slug:slug>/', views.page_detail, name='page-detail'),
]
