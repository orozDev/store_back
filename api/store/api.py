from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny

from store.models import Category, Tag, ProductAttribute, ProductItem, ProductItemImage, Product
from utils.constants import DEFAULT_PERMISSION
from .serializers import CategorySerializer, TagSerializer, ProductAttributeSerializer, \
    ProductItemImageSerializer, CreateProductItemSerializer, ListProductItemSerializer, ProductItemSerializer, \
    DetailProductItemSerializer, CreateUpdateProductSerializer, ListProductSerializer, DetailProductSerializer, \
    ReadCategorySerializer
from ..mixins import UltraModelViewSet, UltraReadOnlyModelViewSet
from ..paginations import StandardResultsSetPagination
from ..permissions import IsSuperAdmin, IsOwnerProduct, IsOwnerProductItem, IsOwner


class CategoryViewSet(UltraModelViewSet):
    queryset = Category.objects.all()
    serializer_classes = {
        'create': CategorySerializer,
        'update': CategorySerializer,
        'list': ReadCategorySerializer,
        'retrieve': ReadCategorySerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['name']
    permission_classes_by_action = DEFAULT_PERMISSION


class TagViewSet(UltraModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['name']
    permission_classes_by_action = DEFAULT_PERMISSION


class ProductAttributeViewSet(UltraModelViewSet):
    queryset = ProductAttribute.objects.all()

    serializer_class = ProductAttributeSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['value', 'name', 'product__name', 'product__description', 'product__content']
    filterset_fields = ['product', 'product__category', 'product__tags']
    permission_classes_by_action = {
        'create': (IsAuthenticated, IsSuperAdmin),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsOwnerProduct),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsOwnerProduct),
    }


class ProductItemImageViewSet(UltraModelViewSet):
    queryset = ProductItemImage.objects.all()
    serializer_class = ProductItemImageSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['product_item__product__name', 'product_item__product__description',
                     'product_item__product__content', 'product_item__name']
    filterset_fields = ['product_item', 'product_item__product']
    permission_classes_by_action = {
        'create': (IsAuthenticated, IsSuperAdmin),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsOwnerProductItem),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsOwnerProductItem),
    }


class ProductItemViewSet(UltraModelViewSet):
    queryset = ProductItem.objects.all()
    serializer_classes = {
        'create': CreateProductItemSerializer,
        'list': ListProductItemSerializer,
        'update': ProductItemSerializer,
        'retrieve': DetailProductItemSerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['product__name', 'product__description', 'product__content', 'color', 'name']
    filterset_fields = ['product', 'product__category', 'product__tags', 'product__user']
    permission_classes_by_action = {
        'create': (IsAuthenticated, IsSuperAdmin),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsOwnerProduct),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsOwnerProduct),
    }

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.method == 'GET':
            return qs.filter(product__is_published=True)
        return qs


class ProductViewSet(UltraModelViewSet):
    queryset = Product.objects.all()
    serializer_classes = {
        'create': CreateUpdateProductSerializer,
        'list': ListProductSerializer,
        'update': CreateUpdateProductSerializer,
        'retrieve': DetailProductSerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['name', 'description', 'content', 'color', 'name']
    filterset_fields = ['category', 'tags', 'is_published', 'user']
    permission_classes_by_action = {
        'create': (IsAuthenticated,),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsOwner),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsOwner),
    }

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.method == 'GET':
            return qs.filter(is_published=True)
        return qs


class OwnProductViewSet(UltraReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_classes = {
        'list': ListProductSerializer,
        'retrieve': DetailProductSerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['name', 'description', 'content', 'color', 'name']
    filterset_fields = ['category', 'tags', 'is_published']
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
    }

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class OwnProductItemViewSet(UltraReadOnlyModelViewSet):
    queryset = ProductItem.objects.all()
    serializer_classes = {
        'list': ListProductItemSerializer,
        'retrieve': DetailProductItemSerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['product__name', 'product__description', 'product__content', 'color', 'name']
    filterset_fields = ['product', 'product__category', 'product__tags']
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
    }

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(product__user=self.request.user)