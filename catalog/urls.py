from django.urls import path

from catalog.views import home, contacts, CatalogDetailView, CatalogListView, BlogDetailView, BlogView, BlogUpdateView, \
    BlogCreateView, BlogDeleteView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contact'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('product/<int:pk>/', CatalogDetailView.as_view(), name='product'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/<str:slug>/', BlogDetailView.as_view(), name='blog_article',),
    path('blog/update/<str:slug>/', BlogUpdateView.as_view(), name='blog_update',),
    path('blog/delete/<str:slug>/', BlogDeleteView.as_view(), name='blog_delete',),

]
