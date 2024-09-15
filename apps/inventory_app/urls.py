# inventory_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Register your viewsets with the router here
# router.register(r'products', views.ProductViewSet)



router = DefaultRouter()

router.register("products", views.ProductViewSet, basename="Products")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/inventory-report/', views.inventory_report, name='inventory_report')
]+ router.urls