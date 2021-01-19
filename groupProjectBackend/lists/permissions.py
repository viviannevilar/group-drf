from rest_framework import permissions
from .models import Collection

class IsOwner(permissions.BasePermission):
   def has_object_permission(self, request, view, obj):
      return obj.user == request.user


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
  def has_permission(self, request, view):
    is_admin = super(
        IsAdminUserOrReadOnly, 
        self).has_permission(request, view)
    return request.method in permissions.SAFE_METHODS or is_admin


class HasOwnerPermissionOrIsOwner(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.allowed_users.filter(id=request.user.id).exists() or obj.user == request.user

class IsOwnerCollectionOrHasPermission(permissions.BasePermission):
  def has_permission(self, request, view):
    collection = Collection.objects.get(pk=view.kwargs['collection'])
    return collection.allowed_users.filter(id=request.user.id).exists() or collection.user == request.user


