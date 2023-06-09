from django.contrib import admin

from catalog.models import Product, Category, Blog


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',)


@admin.register(Blog)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_name', 'slug', 'content', 'data_creating', 'is_published', 'view_count',)
    prepopulated_fields = {'slug': ('title_name',)}
