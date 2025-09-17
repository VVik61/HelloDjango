# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User


class SimpleUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(
        max_length=20,
        required=True,
        help_text='Формат: +7(XXX)XXX-XX-XX'
    )

    agree_personal_data = forms.BooleanField(
        required=True,
        label='Согласен с обработкой персональных данных'
    )

    agree_rules = forms.BooleanField(
        required=True,
        label='Согласен с правилами сайта'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2',
                  'agree_personal_data', 'agree_rules')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.role = 'patient'

        if commit:
            user.save()
        return user


# Временно используем упрощенную форму
UserRegistrationForm = SimpleUserRegistrationForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(
        max_length=16,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '+7(___)___-__-__',
            'class': 'phone-input',
            'data-mask': '+7(000)000-00-00'
        }),
        help_text='Формат: +7(XXX)XXX-XX-XX'
    )

    specialization = forms.CharField(
        max_length=100,
        required=True,
        label='Специализация',
        help_text='Например: Кардиолог, Терапевт, Хирург и т.д.'
    )

    # Добавляем обязательные чекбоксы
    agree_personal_data = forms.BooleanField(
        required=True,
        label='Согласен с обработкой персональных данных',
        error_messages={'required': 'Вы должны согласиться с обработкой персональных данных'}
    )
    
    agree_rules = forms.BooleanField(
        required=True,
        label='Согласен с правилами сайта',
        error_messages={'required': 'Вы должны согласиться с правилами сайта'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'specialization', 'password1', 'password2', 'agree_personal_data', 'agree_rules')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.startswith('+7'):
            raise ValidationError("Номер должен начинаться с +7")
        if len(phone.replace(' ', '')) != 16:
            raise ValidationError(
                "Неверный формат номера. Используйте +7(XXX)XXX-XX-XX")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.role = 'patient'  # Устанавливаем роль по умолчанию
        
        if commit:
            user.save()
        return user