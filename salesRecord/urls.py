from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('findSalesRecord', views.findSalesRecord, name=''),
    path('compare', views.compare, name=''),
]
