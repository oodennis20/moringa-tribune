from rest_framework.permissions import SAFE_METHODS,BasePermission

class IsAdminReadOnly(BasePermission):
  def has_permission(self, request, views):
    if request.method in SAFE_METHODS:
      return True
    else:
      return request.user.is_staff
      
