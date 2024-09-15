from django.contrib import admin
from django.contrib import messages

from apps.inventory_app.utilities import log_stock_change 
from .models import Category, Product, StockChange, Supplier,Alert
class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            original_product = Product.objects.get(pk=obj.pk)
            original_quantity = original_product.quantity
            new_quantity = obj.quantity

            stock_difference = log_stock_change(obj, original_quantity, new_quantity, source="admin pannel")

            if stock_difference != 0:
                messages.info(request, f"Stock changed from {original_quantity} to {new_quantity} for product {obj.name}.")
        
        super().save_model(request, obj, form, change)

        if obj.is_low_stock():
            messages.warning(request, f"Product {obj.name} is low on stock!")

class AlertAdmin(admin.ModelAdmin):
    list_display = ('product', 'message', 'created_at', 'is_seen')

    def changelist_view(self, request, extra_context=None):
        unseen_alerts = Alert.objects.filter(is_seen=False)

        unseen_alerts.update(is_seen=True)

        extra_context = extra_context or {}
        extra_context['unseen_alerts'] = unseen_alerts
        return super(AlertAdmin, self).changelist_view(request, extra_context=extra_context)

admin.site.register(Alert, AlertAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(StockChange)