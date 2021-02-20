from django.urls import path

from . import views

urlpatterns = [
    path('', views.add_geocodes_to_addresses, name='index'),
]