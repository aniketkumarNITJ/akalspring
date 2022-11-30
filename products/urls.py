from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('addproduct', views.addProduct, name='addProd'),
    path('deleteProd', views.delProduct, name='delProd'),
    path('editProd', views.editProduct, name='editProd'),
]
