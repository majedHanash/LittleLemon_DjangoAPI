from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from .permissions import IsManager
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
# Create your views here.

class MenuitemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsManager]
        return super().get_permissions()

    pagination_class = PageNumberPagination
    pagination_class.page_size_query_param = 'perpage'

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        to_price = self.request.query_params.get('to_price')
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        if search:
            queryset = queryset.filter(title__contains=search)
        if to_price:
            queryset = queryset.filter(price__lte=to_price)
        if category:
            queryset = queryset.filter(category__title__iexact=category)
        return queryset

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method != 'GET':
            self.permission_classes = [IsManager]
        return super().get_permissions()

