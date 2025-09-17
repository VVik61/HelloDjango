from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date

def validate_birth_date(value):
    if value < date(1920, 1, 1):
        raise ValidationError('Дата рождения не может быть раньше 1920 года')
    if value > date.today():
        raise ValidationError('Дата рождения не может быть в будущем')

class Question(models.Model):
    text = models.TextField(verbose_name="Текст вопроса")
    explanation = models.TextField(
        verbose_name="Пояснение к вопросу",
        blank=True,
        help_text="Пояснительный текст, который будет отображаться под вопросом"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активный вопрос")

    class Meta:
        verbose_name = "Вопрос анкеты"
        verbose_name_plural = "Вопросы анкеты"
        ordering = ['order']

    def __str__(self):
        return self.text

class Anketa(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        validators=[validate_birth_date]
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Пол"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заполнения")
    answers_text = models.TextField(verbose_name="Текст ответов")

    class Meta:
        verbose_name = "Заполненная анкета"
        verbose_name_plural = "Заполненные анкеты"
        ordering = ['-created_at']

    def __str__(self):
        return f"Анкета {self.full_name} от {self.created_at.strftime('%d.%m.%Y')}"

    def generate_answers_text(self, form_data):
        answers_text = []
        answers_text.append(f"ФИО: {self.full_name}")
        answers_text.append(f"Дата рождения: {self.birth_date.strftime('%d.%m.%Y')}")
        answers_text.append(f"Пол: {self.get_gender_display()}")
        answers_text.append(f"Дата заполнения: {self.created_at.strftime('%d.%m.%Y')}\n")
        
        questions = Question.objects.filter(is_active=True).order_by('order')
        no_answers = []
        
        for question in questions:
            answer_key = f'question_{question.id}'
            comment_key = f'comment_{question.id}'
            
            if answer_key in form_data and form_data[answer_key] == 'yes':
                answers_text.append(f"{question.text} - ДА")
                if form_data.get(comment_key):
                    answers_text.append(f"Дополнительные сведения: {form_data[comment_key]}")
                answers_text.append("")
            else:
                no_answers.append(question.text)
        
        if no_answers:
            answers_text.append("\nОтветы на следующие вопросы - НЕТ:")
            for q_text in no_answers:
                answers_text.append(q_text)
            # answers_text.append("-НЕТ")
        
        self.answers_text = "\n".join(answers_text)
        with open('e:rez_anketa.txt', 'w') as f:
            f.writelines(self.answers_text)
        self.save()
        return self.answers_text