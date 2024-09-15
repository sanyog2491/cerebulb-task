from celery import shared_task
from .models import Product, Alert

@shared_task
def check_low_stock():
    low_stock_products = Product.objects.filter(quantity__lt=5)
    for product in low_stock_products:
        Alert.objects.create(product=product, message=f"Re-Alert For Low stock: {product.name} is below 5 units.")
