from django.conf.urls import url, include
from django.urls import path

from . import views
app_name = 'inventory'
urlpatterns = [
    path('listEquipment/', views.EquipmentListView.as_view(), name='listEquipment'),
    path('detailEquipment/<int:pk>', views.EquipmentDetailsView.as_view(), name='detailEquipment'),
    path('createHandover/<int:pk>', views.createHandover, name='createHandover'),
]
