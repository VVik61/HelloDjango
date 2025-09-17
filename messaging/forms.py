# messaging/forms.py
from django import forms
from .models import PrivateMessage
from users.models import User

class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите тему сообщения'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст сообщения',
                'rows': 5
            }),
            'recipient': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'recipient': 'Получатель',
            'subject': 'Тема',
            'body': 'Сообщение'
        }

    def __init__(self, *args, **kwargs):
        # Убираем всю логику с пользователем до сохранения
        super().__init__(*args, **kwargs)
        
        # Устанавливаем базовый queryset
        self.fields['recipient'].queryset = User.objects.filter(
            role__in=['doctor', 'patient']
        )

    def clean_recipient(self):
        """Валидация получателя происходит после сохранения пользователя"""
        recipient = self.cleaned_data.get('recipient')
        # Здесь можно добавить дополнительную валидацию если нужно
        return recipient