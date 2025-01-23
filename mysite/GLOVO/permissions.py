from rest_framework import permissions


class CheckOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'владелец магазина':
            return True
        return False

class CheckOwnerEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner



class CheckClient(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'клиент':
            return True
        return False

























