from django.conf.urls import url, include
from django.urls import path

from . import views
app_name = 'networkmap'
urlpatterns = [
    path('', views.index, name='index'),
    path('addDevice/', views.addDevice, name='addDevice'),
    path('editDevice/<int:id>', views.editDevice, name='editDevice'),
    path('deviceList/', views.DeviceListView.as_view(), name='listDevices'),
    path('deviceNextHop/', views.DeviceListView.as_view()),
#    url('listDevices/', views., name='addDevice'),
]
