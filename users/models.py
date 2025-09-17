from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.core.exceptions import ValidationError
import re
from datetime import date

class User(AbstractUser):
    ROLES = (
        ('admin', 'Администратор'),
        ('editor', 'Редактор'),
        ('doctor', 'Врач'),
        ('medsestra', 'Медсестра'),
        ('patient', 'Пациент')
    )

    role = models.CharField(
        max_length=10, 
        choices=ROLES, 
        default='patient',
        verbose_name='Роль'
    )
    assigned_doctor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to=Q(role='doctor'),
        related_name='doctor_patients',
        verbose_name='Лечащий врач'
    )
    specialization = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Специализация'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Номер телефона',
        help_text='Формат: +7(XXX)XXX-XX-XX'
    )
    social_auth = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Данные социальных сетей'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Аккаунт активен'
    )
    registration_completed = models.BooleanField(
        default=False,
        verbose_name='Регистрация завершена'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='Группы',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
        help_text='Группы, к которым принадлежит пользователь.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='Права пользователя',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
        help_text = 'Конкретные права для этого пользователя.'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['phone'],
                name='unique_phone',
                condition=Q(phone__isnull=False),
            ),
        ]

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        # Упростим валидацию для отладки
        if self.phone:
            # Временно отключим строгую валидацию
            pass

    def save(self, *args, **kwargs):
        # Упростим логику сохранения для отладки
        if self.role == 'patient':
            self.is_active = True

        if not self.pk and self.role in ['doctor', 'medsestra']:
            self.is_active = False

        # Временно отключим форматирование телефона
        super().save(*args, **kwargs)




    # def get_role_display(self):
    #     """Возвращает читаемое название роли"""
    #     return dict(self.ROLES).get(self.role, self.role)
    #
    # @property
    # def assigned_patients(self):
    #     """Возвращает пациентов врача"""
    #     if self.role == 'doctor':
    #         return self.doctor_patients.all()
    #     return User.objects.none()
    #
    # @property
    # def assigned_doctors(self):
    #     """Возвращает врачей пациента"""
    #     if self.role == 'patient':
    #         return User.objects.filter(doctor_patients=self)
    #     return User.objects.none()

    # def clean(self):
    #     super().clean()
    #     if self.phone:
    #         if not re.match(r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$', self.phone):
    #             raise ValidationError(
    #                 {'phone': 'Номер телефона должен быть в формате +7(XXX)XXX-XX-XX'}
    #             )
    #
    #     if self.role in ['doctor', 'medsestra'] and not self.phone:
    #         raise ValidationError(
    #             {'phone': 'Для медицинских работников номер телефона обязателен'}
    #         )
    #
    #     if self.role == 'patient' and self.assigned_doctors.count() >= 10:
    #         raise ValidationError(
    #             {'assigned_doctor': 'Пациент не может быть прикреплён более чем к 10 врачам'}
    #         )
    #
    # def save(self, *args, **kwargs):
    #     if self.role == 'patient':
    #         self.is_active = True
    #
    #     if not self.pk and self.role in ['doctor', 'medsestra']:
    #         self.is_active = False
    #
    #     if self.phone:
    #         digits = re.sub(r'\D', '', self.phone)
    #         if digits.startswith('8'):
    #             digits = '7' + digits[1:]
    #         if len(digits) == 10:
    #             digits = '7' + digits
    #         self.phone = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:]}"
    #
    #     super().save(*args, **kwargs)