from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from .permissions import IsManager
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class MenuitemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsManager]
        return super().get_permissions()

    pagination_class = PageNumberPagination
    pagination_class.page_size_query_param = 'perpage'
