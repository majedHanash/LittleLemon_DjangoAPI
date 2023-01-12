from django.urls import path
from . import views

urlpatterns = [
    path('menu-items/', views.MenuitemView.as_view()),
    path('menu-items/<int:pk>/', views.MenuItemDetailView.as_view()),
    path('groups/manager/users/', views.ManagerView.as_view()),
    path('groups/delivery-crew/users/', views.DeliveryCrewView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerRemoveView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewRemoveView.as_view()),
]

