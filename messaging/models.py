from django.db import models
from users.models import User

class PrivateMessage(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_private_messages',
        limit_choices_to={'role__in': ['doctor', 'patient']}
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_private_messages',
        limit_choices_to={'role__in': ['doctor', 'patient']}
    )
    subject = models.CharField(max_length=200, default='Без темы')  # Добавлено default
    body = models.TextField(default='')  # Пустая строка как default
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Приватное сообщение'
        verbose_name_plural = 'Приватные сообщения'

    def __str__(self):
        return f"{self.subject} (от {self.sender} к {self.recipient})"