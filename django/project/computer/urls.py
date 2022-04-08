from django.urls import path, include

from . import views
app_name = 'computer'
urlpatterns = [
    path('lizenzList/', views.LizenzListView.as_view(), name='lizenzList'),
]