from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

class MenuItem(models.Model):
    INTERNAL_LINK_CHOICES = [
        ('', '-- Не выбрано --'),
        ('home', 'Главная страница'),
        ('about', 'О нас...'),
        ('login', 'Вход учётную запись'),
        ('anketa/start', 'Анамнез при госпитализации'),
        ('contacts', 'Контакты'),
        ('vozmogm', 'Диагностические возможности'),
    ]
    
    # Основные поля
    title = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name='children', verbose_name="Родительский пункт")
    order = models.PositiveIntegerField(default=0)
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Поля для ссылок
    is_content_page = models.BooleanField(default=True)
    internal_link = models.CharField(
        max_length=20,
        choices=INTERNAL_LINK_CHOICES,
        blank=True
    )
    custom_slug = models.SlugField(blank=True)
    url = models.CharField(max_length=200, blank=True)
    
    # Контент
    content = CKEditor5Field(config_name='extends', blank=True)
    
    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if not self.is_content_page and self.url:
            return self.url
        if self.internal_link:
            try:
                # print(self.internal_link)
                return reverse(self.internal_link)
            except:
                # Если маршрут не найден, возвращаем "/"
                return '/'
        if self.custom_slug:
            return reverse('page-detail', kwargs={'slug': self.custom_slug})
        return reverse('menu-content', kwargs={'pk': self.id})

    @property
    def has_children(self):
        """Проверяет, есть ли подпункты меню"""
        return self.children.exists()
    
    def __str__(self):
        return self.title