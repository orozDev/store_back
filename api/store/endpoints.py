from rest_framework import routers
from django.urls import path, include
from . import api

router = routers.DefaultRouter()
router.register('categories', api.CategoryViewSet)
router.register('tags', api.TagViewSet)

product_item_router = routers.DefaultRouter()
product_item_router.register('images', api.ProductItemImageViewSet)
product_item_router.register('own', api.OwnProductItemViewSet)
product_item_router.register('', api.ProductItemViewSet)

product_router = routers.DefaultRouter()
product_router.register('attributes', api.ProductAttributeViewSet)
product_router.register('own', api.OwnProductViewSet)
product_router.register('', api.ProductViewSet)

urlpatterns = [
    path('products/items/', include(product_item_router.urls)),
    path('products/', include(product_router.urls)),
    path('', include(router.urls)),
]
