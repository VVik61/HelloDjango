from django import forms
from django.forms import DateInput
from datetime import date
from .models import Question


class AnketaForm(forms.Form):
    full_name = forms.CharField(
        label='ФИО*',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше полное имя'
        })
    )
    birth_date = forms.DateField(
        label='Дата рождения*',
        widget=DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'min': '1920-01-01',
                'max': date.today().strftime('%Y-%m-%d')
            },
            format='%Y-%m-%d'
        )
    )
    gender = forms.ChoiceField(
        label='Пол*',
        choices=[('M', 'Мужской'), ('F', 'Женский')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='M'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = Question.objects.filter(is_active=True).order_by('order')

        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                help_text=question.explanation,
                choices=[('yes', 'Да'), ('no', 'Нет')],
                widget=forms.RadioSelect(attrs={
                    'class': 'form-check-input',
                }),
                required=True
            )
            self.fields[f'comment_{question.id}'] = forms.CharField(
                label='',
                widget=forms.Textarea(attrs={
                    'cols': 80,
                    'rows': 1,
                    'class': 'form-control comment-field',
                    'placeholder': 'Уточните ваш ответ (если требуется)',
                    'id': f'id_comment_{question.id}'
                }),
                required=False
            )