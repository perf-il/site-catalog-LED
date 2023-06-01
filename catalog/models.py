from datetime import datetime

from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):

    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f"{self.name}, {self.description}"


class Product(models.Model):

    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='preview', default='preview/default.JPG')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', **NULLABLE)
    price = models.FloatField(verbose_name='Цена')
    data_creating = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    data_updating = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения', **NULLABLE)

    def __str__(self):
        return f"{self.name}, {self.category}"
