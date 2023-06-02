import json

from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        #удаление объектов из моделей
        Category.objects.all().delete()
        Product.objects.all().delete()

        #загрузка данных из файла для модели Catalog
        with open('.\catalog\data\catalog_data.json') as f:
            data_category = json.load(f)
        category_list = []
        for category in data_category:
            category_id = category.get("pk")
            field = category.get('fields')
            name = field.get('name')
            description = field.get('description')

            category_list.append(Category(name=name,
                                          description=description,
                                          pk=category_id))

        #создание новых объектов в модели Catalog
        Category.objects.bulk_create(category_list)

        #загрузка данных из файла для модели Product
        with open('.\catalog\data\product_data.json') as f:
            data_product = json.load(f)
        product_list = []
        for i, product in enumerate(data_product):

            product_id = i + 1
            field = product.get('fields')
            name = field.get('name')
            description = field.get('description')
            preview = field.get('preview')
            category = Category.objects.get(pk=field.get('category'))
            price = field.get('price')
            data_creating = field.get('data_creating')
            data_updating = field.get('data_updating')

            product_list.append(Product(name=name,
                                        description=description,
                                        preview=preview,
                                        category=category,
                                        price=price,
                                        data_creating=data_creating,
                                        data_updating=data_updating,
                                        pk=product_id))

        #создание новых объектов в модели Product
        Product.objects.bulk_create(product_list)

        print('Loading successfully')
