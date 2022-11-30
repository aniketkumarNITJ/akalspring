from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('addBill', views.addBill, name='billAdd'),
    path('allBills', views.showBills, name='allBills'),
    path('deleteBill', views.deleteBill, name='delBills'),
    path('editBill', views.editBill, name='editBill'),
    path('saveEdit', views.editSave, name='saveEdit'),
]
