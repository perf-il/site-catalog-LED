from django.urls import path

from catalog.views import home, contacts, about_me

urlpatterns = [
    path('', home),
    path('contacts/', contacts),
    path('about/', about_me),

]
