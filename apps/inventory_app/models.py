from django.db import models
from django.contrib.auth.models import User
from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
        
    def is_low_stock(self):
        return self.quantity < 5
    
    def save(self, *args, **kwargs):
        # Get the previous product instance before saving
        if self.pk:
            original_product = Product.objects.get(pk=self.pk)
            print("original_product",original_product)
            original_quantity = original_product.quantity
            print("original_quantity",original_quantity)
        else:
            original_quantity = None

        super(Product, self).save(*args, **kwargs)  # Save the product first

        # If the quantity is below 5, create an alert
        if self.is_low_stock():
            # If quantity is changed and now it's low, create an alert
            if original_quantity is None or original_quantity >= 5 or original_quantity <= 5:
                Alert.objects.create(
                    product=self,
                    message=f"Product {self.name} is low on stock. Only {self.quantity} left!"
                )
                
        # If quantity was low before and now it’s updated above 5, remove the alert (if desired)
        if original_quantity is not None and original_quantity < 5 and self.quantity >= 5:
            Alert.objects.filter(product=self, is_seen=False).update(is_seen=True)

class StockChange(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_changed = models.IntegerField()
    date_of_change = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.product.name} - {self.quantity_changed} ({self.reason})"


class Alert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.message
