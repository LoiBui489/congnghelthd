from rest_framework import permissions

from .properties import ROLE_ADMIN, ROLE_SHOP


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return request.user and request.user.role == ROLE_ADMIN


class IsShopPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == ROLE_SHOP


class IsOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user
