from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages import success
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from pytils.translit import slugify

from catalog.forms import ProductForm, ProductVersionForm
from catalog.models import Product, Blog, ProductVersion


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


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Blog
    fields = ['title_name', 'content', 'preview']
    success_url = reverse_lazy('catalog:blog')
    extra_context = {
        'title': 'Написать статью'
    }

    def form_valid(self, form):
        if form.is_valid():
            fields = form.save(commit=False)
            fields.slug = slugify(form.cleaned_data['title_name'])
            fields.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    fields = ['title_name', 'content', 'preview']
    success_url = reverse_lazy('catalog:blog')
    extra_context = {
        'title': 'Редактировать статью'
    }


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog')
    extra_context = {
        'title': 'Удалить статью'
    }


class ProductCreateView(LoginRequiredMixin, generic.CreateView):

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:catalog')


    def form_valid(self, form):
        if form.is_valid():
            fields = form.save(commit=False)
            fields.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:catalog')
    permission_required = 'catalog.change_product'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, ProductVersion, form=ProductVersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user.has_perm('catalog.change_product'):
            return self.object
        if self.object.created_by != self.request.user:
            raise Http404('Нет прав доступа')
        return self.object


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:catalog')
    permission_required = 'catalog.change_product'
    extra_context = {
        'title': 'Удалить продукт'
    }

