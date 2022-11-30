from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('allBills', views.showBills, name='allBills'),
    path('pdf', views.showPdf, name=''),
    # path('getPdf', views.some_view, name='')
]
