from django.conf.urls import url, include
from django.urls import path

from . import views
app_name = 'computer'
urlpatterns = [
    path('lizenzList/', views.LizenzListView.as_view(), name='lizenzList'),
]