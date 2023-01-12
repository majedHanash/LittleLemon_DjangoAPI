from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import MenuItem, Category
from rest_framework.validators import UniqueValidator


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price', 'featured', 'category','category_id']
        extra_kwargs = {
                'title': {
                    'validators': [
                        UniqueValidator(
                            queryset=MenuItem.objects.all()
                        )
                    ]
                },
            }
    def validate(self, attrs):
        if 'price' in attrs and attrs['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return super().validate(attrs)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email']
        extra_kwargs = {'std_code': {'required': False}}