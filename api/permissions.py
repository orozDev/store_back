from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser


class IsSuperAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_superuser


class IsOwnerComment(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.email == obj.email or request.user.is_superuser


class IsOwnerCommentImage(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.comment.user or request.user.is_superuser


class IsOwnerProduct(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.product.user or request.user.is_superuser


class IsOwnerProductItem(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.product_item.product.user or request.user.is_superuser
