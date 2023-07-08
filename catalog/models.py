from datetime import datetime
from transliterate import slugify

from django.db import models

from users.models import User, NULLABLE


class Category(models.Model):

    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):

    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='preview', default='preview/default.JPG', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', **NULLABLE)
    price = models.FloatField(verbose_name='Цена')
    data_creating = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    data_updating = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения', **NULLABLE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Добавлено', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='опубликовано')

    def __str__(self):
        return f"{self.name}, {self.category}"


class Blog(models.Model):

    title_name = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(default=slugify(str(title_name)), max_length=150)
    content = models.TextField(verbose_name='Текст', **NULLABLE)
    preview = models.ImageField(upload_to='blog/preview', default='preview/default.JPG', verbose_name='Изображение')
    data_creating = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    view_count = models.IntegerField(default=0)

    def add_view(self):
        self.view_count += 1
        return self.view_count

    def delete(self, *args, **kwargs):
        self.is_published = False
        self.save()

    def __str__(self):
        return f"{self.title_name}"


class ProductVersion(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='version')
    version_number = models.PositiveIntegerField(verbose_name='Номер версии', **NULLABLE)
    version_name = models.CharField(max_length=50, verbose_name='Имя версии', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Активная версия')

    def __str__(self):
        return f'{self.version_number}'

