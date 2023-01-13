from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem, Cart
from .serializers import MenuItemSerializer, UserSerializer, AddCartSerializer, GetCartSerializer
from .permissions import IsManager
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

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

class GroupView(APIView):
    group = None
    def get(self, request):
        users = User.objects.filter(groups__name=self.group)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            assign_group = Group.objects.get(name=self.group)
            assign_group.user_set.add(user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({'username':'this field is required'} ,status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return super().get_queryset()
    

    def get_permissions(self):
        self.permission_classes = [IsManager]
        return super().get_permissions()

class ManagerView(GroupView):
    group = 'Manager'
class DeliveryCrewView(GroupView):
    group = 'Delivery Crew'

class GroupRemoveView(APIView):
    group = None
    def delete(self, request, pk, format=None):
        user = get_object_or_404(User,id=pk)
        if not user.groups.filter(name=self.group):
            return Response('user with id: ' + str(pk) + ' is not a ' + self.group, status=status.HTTP_400_BAD_REQUEST)
            
        assign_group = Group.objects.get(name=self.group)
        assign_group.user_set.remove(user)
        return Response(status=status.HTTP_200_OK)

    def get_permissions(self):
        self.permission_classes = [IsManager]
        return super().get_permissions()
class ManagerRemoveView(GroupRemoveView):
    group = 'Manager'
class DeliveryCrewRemoveView(GroupRemoveView):
    group = 'Delivery Crew'

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = AddCartSerializer
    def get(self, request, format=None):
        carts = Cart.objects.filter(user__id=request.user.id)
        serializer = GetCartSerializer(carts, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
        
    def destroy(self, request, *args, **kwargs):
        Cart.objects.filter(user__id=request.user.id).delete()
        return Response(status=status.HTTP_200_OK)
