from django.conf.urls import url, include
from django.urls import path, register_converter

from . import views, converters

register_converter(converters.NegativeIntConverter, 'negint')

app_name = 'networkmap'
urlpatterns = [
    path('', views.index, name='index'),
    path('addDevice/', views.addDevice, name='addDevice'),
    path('editDevice/<int:id>', views.editDevice, name='editDevice'),
    path('deviceList/', views.DeviceListView.as_view(), name='listDevices'),
    path('deviceNextHop/', views.nextHop),
    path('showRoom', views.showRoom, name='showNewRoom'),
    path('showRoom/<int:id_room>', views.showRoom, name='showRoom'),
    path('saveRoom/<negint:id_room>', views.saveRoom, name='saveRoom'),
    path('listRoom', views.ListRoomView.as_view(), name='listRoom'),

    path('connectPort/', views.connectPort, name='connectPort'),
    path('connectPort/<int:id_port>', views.connectPort, name='connectPortById'),
#    url('listDevices/', views., name='addDevice'),
]
