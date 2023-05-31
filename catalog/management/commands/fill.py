import json

from django.core.management import BaseCommand
from catalog.models import Product, Category
import psycopg2


class Command(BaseCommand):
    connect = psycopg2.connect(
        host="localhost",
        database="catalog",
        user="postgres",
        password="4444"
    )

    def handle(self, conn=connect, *args, **options):
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"TRUNCATE catalog_product RESTART IDENTITY;"
                            f"TRUNCATE catalog_category RESTART IDENTITY CASCADE;\n")
            print('Tables catalog_product and catalog_category were cleared')

        with open('.\catalog\data\catalog_data.json') as f:
            data_category = json.load(f)
        category_list = []
        for table in data_category:
            category_list.append(Category(**table.get('fields')))

        Category.objects.bulk_create(category_list)

        with open('.\catalog\data\product_data.json') as f:
            data_product = json.load(f)
        product_list = []
        for product in data_product:
            product_list.append(Product(**product.get('fields')))

        Product.objects.bulk_create(product_list)

        print('Loading successfully')
