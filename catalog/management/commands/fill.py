from django.core.management import BaseCommand
import psycopg2
import os


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
                cur.execute(f"TRUNCATE catalog_product;"
                            f"TRUNCATE catalog_category CASCADE;\n")
            print('Tables catalog_product and catalog_category were cleared')
        os.system('python manage.py loaddata .\catalog\data\catalog_data.json')
        os.system('python manage.py loaddata .\catalog\data\product_data.json')
        print('Loading successfully')
