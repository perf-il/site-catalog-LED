from django.shortcuts import render

from catalog.models import Product


def home(request):
    product_list = Product.objects.all()
    context = {
        'product_list': product_list,
        'title': 'Каталог'
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} ({phone}): {message}')

    context = {
        'title': 'Контакты'
    }

    return render(request, 'catalog/contacts.html', context)


def product_card(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'object': product,
        'title': product.name
    }
    return render(request, 'catalog/product_card.html', context)
