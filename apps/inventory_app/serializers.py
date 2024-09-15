# inventory_app/serializers.py
from rest_framework import serializers
from .models import Category, Supplier, Product,StockChange

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
class StockChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockChange
        fields = '__all__'

