from django.shortcuts import render

from catalog.models import Product


def home(request):
    product_list = Product.objects.all()
    context = {
        'product_list': product_list
    }
    return render(request, 'catalog\\home.html', context)


def contacts(request):
    return render(request, 'catalog\\contacts.html')


def about_me(request):
    return render(request, 'catalog\\about_me.html')
