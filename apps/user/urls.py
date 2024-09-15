# inventory_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


router.register("login", views.LoginApi, basename="Log In")
router.register("register", views.RegisterViewset, basename="Log In")

urlpatterns = [
    path('', include(router.urls)),
]+ router.urls
