from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.inventory_app.utilities import log_stock_change
from apps.user.customs.permissions import  custom_permission_required
from apps.user.models import Page
from .models import Category, Product, Supplier
from .serializers import ProductSerializer
from rest_framework.decorators import action

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()

    @custom_permission_required(page_name="product", action="add")
    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            response = {
                "message": "Product created successfully",
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
            }
            return Response(response, status=status.HTTP_201_CREATED, headers=headers)
        response = {
            "message": serializer.errors.get(next(iter(serializer.errors)))[0],
            "data": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    @custom_permission_required(page_name="product", action="edit")
    def update(self, request, *args, **kwargs):
        try:
            instance = Product.objects.get(id=kwargs["pk"])
        except Product.DoesNotExist:
            return Response(
                {
                    "message": "Product not found.",
                    "status": status.HTTP_404_NOT_FOUND,
                },
            )
        original_quantity = instance.quantity
        print("original_quantity",original_quantity)
        serializer = ProductSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                product = serializer.save()
                
                new_quantity = product.quantity
                print("new_quantity",new_quantity)
                # Log stock changes
                log_stock_change(product, original_quantity, new_quantity, source="api")
                response = {
                    "message": "Product updated successfully",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                }
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                response = {
                    "message": "Failed to update product due to server error.",
                    "error": str(e),
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = {
            "message": serializer.errors.get(next(iter(serializer.errors)), "Invalid data"),
            "data": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    
    @custom_permission_required(page_name="product", action="delete")
    def destroy(self, request, *args, **kwargs):

        try:
            instance = self.get_object()
        except Product.DoesNotExist:
            return Response(
                {
                    "message": "Product not found.",
                    "status": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        instance.delete()

        return Response(
            {
                "message": "Product deleted successfully.",
                "status": status.HTTP_204_NO_CONTENT,
            },
            status=status.HTTP_204_NO_CONTENT,
        )



def inventory_report(request):
    # Total inventory value (sum of product quantities * price)
    total_inventory_value = sum([product.quantity * product.price for product in Product.objects.all()])
    
    # Filters
    category = request.GET.get('category')
    supplier = request.GET.get('supplier')
    stock_level = request.GET.get('stock_level')
    order = request.GET.get('order', 'asc')  
    products = Product.objects.all()

    if category:
        products = products.filter(category__id=category)
    if supplier:
        products = products.filter(supplier__id=supplier)
    if stock_level:
        products = products.filter(quantity__gte=stock_level)

    if order == 'asc':
        products = products.order_by('quantity')
    else:
        products = products.order_by('-quantity')

    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    context = {
        'total_inventory_value': total_inventory_value,
        'filtered_products': products,
        'categories': categories,
        'suppliers': suppliers,
        'order': order,  # Pass the current sorting order to the template
    }
    return render(request, 'admin/inventory_report.html', context)

