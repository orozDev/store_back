from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.mixins import SuperModelViewSet
from api.paginations import StandardResultsSetPagination
from api.permissions import IsOwnerComment, IsOwnerCommentImage
from api.serializers import CommentSerializer, CommentImageSerializer
from core.models import Comment, CommentImage


class CommentViewSet(SuperModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['name', 'email', 'text']
    filterset_fields = ['product']
    permission_classes_by_action = {
        'create': (AllowAny,),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsOwnerComment,),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsOwnerComment,),
    }


class CommentImageViewSet(SuperModelViewSet):
    queryset = CommentImage.objects.all()
    serializer_class = CommentImageSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    filterset_fields = ['comment']
    permission_classes_by_action = {
        'create': (AllowAny,),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsOwnerCommentImage,),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsOwnerCommentImage,),
    }
