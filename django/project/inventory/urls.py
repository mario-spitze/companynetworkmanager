from django.conf.urls import url, include
from django.urls import path

from . import views
app_name = 'inventory'
urlpatterns = [
    path('createHardwareClass/', views.HardwareClassCreateView.as_view(), name='createHardwareClass'),
    path('updateHardwareClass/<int:pk>', views.HardwareClassUpdateView.as_view(), name='updateHardwareClass'),
    path('listHardwareClass/', views.HardwareClassListView.as_view(), name='listHardwareClass'),
    path('createArticle/', views.createArticle, name='createArticle'),
    path('updateBulkArticle/<int:pk>', views.BulkArticleUpdateView.as_view(), name='updateBulkArticle'),
    path('updateArticle/<int:pk>', views.ArticleUpdateView.as_view(), name='updateArticle'),
    path('listArticle/', views.ArticleListView.as_view(), name='listArticle'),
    path('createEquipment/', views.EquipmentCreateView.as_view(), name='createEquipment'),
    path('updateEquipment/<int:pk>', views.EquipmentUpdateView.as_view(), name='updateEquipment'),
    path('listEquipment/', views.EquipmentListView.as_view(), name='listEquipment'),
    path('detailEquipment/<int:pk>', views.EquipmentDetailsView.as_view(), name='detailEquipment'),
    path('listWorkplace/', views.WorkplaceListView.as_view(), name='listWorkplace'),
    path('detailWorkplace/<int:pk>', views.WorkplaceDetailsView.as_view(), name='detailWorkplace'),
    path('listCustomer/', views.CustomerListView.as_view(), name='listCustomer'),
    path('giveBack/<int:handoverID>', views.giveBack, name='giveBack'),

    path('createHandover/<slug:objType>/<int:pk>/', views.createHandover, name='createHandover'),
]
