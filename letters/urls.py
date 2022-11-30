from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('addData', views.addData, name='billAdd'),
    path('allBills', views.showBills, name='allBills'),
    path('bankLetter', views.bankLetter, name='bankLetter'),
    path('exportOfDeclaration', views.exportDeclaration, name='exportDeclaration'),
    path('billOfExchange', views.billOfExchange, name='billOfExchange'),
    path('edit', views.edit, name='edit'),
    path('saveEdit', views.saveEdit, name='edit'),
    path('bankLetter2', views.bankLetter2, name=''),
    path('shipmentLetter', views.shipmentLetter, name=''),
]
