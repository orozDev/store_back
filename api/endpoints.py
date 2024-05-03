from rest_framework import routers
from django.urls import path, include
from .yasg import urlpatterns as url_doc
from . import api

router = routers.DefaultRouter()
router.register('comments', api.CommentViewSet)
router.register('comments-images', api.CommentImageViewSet)

urlpatterns = [
    path('auth/', include('api.auth.endpoints')),
    path('store/', include('api.store.endpoints')),
    path('', include(router.urls)),
]

urlpatterns += url_doc
