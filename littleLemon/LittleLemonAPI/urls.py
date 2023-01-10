from django.urls import path
from . import views

urlpatterns = [
    path('menu-items/', views.MenuitemView.as_view()),
    path('menu-items/<int:pk>/', views.MenuItemDetailView.as_view()),
]
