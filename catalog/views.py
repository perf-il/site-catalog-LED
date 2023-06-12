from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from pytils.translit import slugify


from catalog.models import Product, Blog


def home(request):
    product_list = Product.objects.all()
    context = {
        'product_list': product_list,
        'title': 'Каталог'
    }
    return render(request, 'catalog/home.html', context)


class CatalogListView(generic.ListView):
    model = Product
    extra_context = {
        'title': 'Каталог'
    }


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


class CatalogDetailView(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


class BlogView(generic.ListView):
    model = Blog
    extra_context = {
        'title': 'Блог'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        queryset = queryset.order_by('-data_creating')
        return queryset


class BlogDetailView(generic.DetailView):
    model = Blog

    def get_object(self, queryset=None):
        post = super().get_object()
        post.add_view()
        post.save()
        return post

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object']

        return context_data


class BlogCreateView(generic.CreateView):
    model = Blog
    fields = ['title_name', 'content', 'preview']
    success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        if form.is_valid:
            fields = form.save(commit=False)
            fields.slug = slugify(form.cleaned_data['title_name'])
            fields.save()
        return super().form_valid(form)


class BlogUpdateView(generic.UpdateView):
    model = Blog
    fields = ['title_name', 'content', 'preview']
    success_url = reverse_lazy('catalog:blog')


class BlogDeleteView(generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog')



