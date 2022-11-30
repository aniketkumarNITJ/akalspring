from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('allBills', views.showBills, name=''),
    path('addProformaInvoice', views.addInvoice, name=''),
    path('pdf', views.getPdf, name=''),
    path('deleteBill', views.deleteBill, name=''),
    path('editBill', views.editBill, name=''),
    path('saveEdit', views.saveEdit, name=''),
    path('changeDescription', views.changeDescription, name=''),
]
