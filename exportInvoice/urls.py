from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('allBills', views.showBills, name='allBills'),
    path('pdf', views.showPdf, name=''),
    path('changeDescri', views.changeDescri),
    path('changeWithComponents', views.changeWithComponents),
    path('changeDescription', views.changeDescription),
    path('changeShippingMark', views.changeShippingMark),
    path('changeCFFOB', views.changeCFFOB),
    path('changeAmtDesc', views.changeAmtDesc),
    path('updatecompName', views.updatecompName),
    path('updateAddress', views.updateAddress),
    path('updateCountry', views.updateCountry),
]
