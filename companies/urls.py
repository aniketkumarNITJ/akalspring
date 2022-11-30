from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('addcompany', views.addCompany, name='addComp'),
    path('deleteComp', views.delCompany, name='delComp'),
    path('editComp', views.editCompany, name='editComp'),
]
