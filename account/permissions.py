from rest_framework import permissions


class IsAuthenticatedOrNotAllowed(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		if request.user.is_authenticated():
			return True
		return False


class IsOwnerOrReadOnly(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return request.user == obj