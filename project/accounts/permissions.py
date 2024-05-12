# -*- coding: utf-8 -*-
# permissions.py
from rest_framework.permissions import SAFE_METHODS, BasePermission



class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is an admin
        # if request.user and request.user.is_superuser:
        if request.user and( request.user.is_staff or request.user.is_superuser):
            return True
        
        if request.method in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # if request.user and request.user.is_superuser:
        if request.user and( request.user.is_staff or request.user.is_superuser):
            return True

        if request.method in SAFE_METHODS:
            return True
        return False

            