from django.contrib import admin
from django.urls import path, include
from products.views import ProductViewSet
from books.views import BookViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
]
