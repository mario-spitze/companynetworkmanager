from django.conf.urls import url, include
from django.urls import path

from . import views
app_name = 'inventory'
urlpatterns = [
    path('listEquipment/', views.EquipmentListView.as_view(), name='listEquipment'),
    path('listWorkplace/', views.WorkplaceListView.as_view(), name='listWorkplace'),
    path('listCustomer/', views.CustomerListView.as_view(), name='listCustomer'),
    path('detailEquipment/<int:pk>', views.EquipmentDetailsView.as_view(), name='detailEquipment'),
    path('createHandover/<slug:objType>/<int:pk>/', views.createHandover, name='createHandover'),
]
