from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Управление пользователями'

    def ready(self):
        """Сигналы подключаем только после полной загрузки"""
        try:
            from . import signals  # Ленивый импорт
        except ImportError:
            pass

