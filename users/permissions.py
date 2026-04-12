from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser


class IsBuyer(permissions.BasePermission):
    """
    Allows access only to buyers.
    """
    
    def has_permission(self, request, view):
        if not request.user or request.user == AnonymousUser():
            return False
            
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role == 'buyer'
        return False


class IsSeller(permissions.BasePermission):
    """
    Allows access only to sellers.
    """
    
    def has_permission(self, request, view):
        if not request.user or request.user == AnonymousUser():
            return False
            
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role == 'seller'
        return False


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admins.
    """
    
    def has_permission(self, request, view):
        if not request.user or request.user == AnonymousUser():
            return False
            
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role == 'admin'
        return False


class IsBuyerOrSeller(permissions.BasePermission):
    """
    Allows access to buyers and sellers.
    """
    
    def has_permission(self, request, view):
        if not request.user or request.user == AnonymousUser():
            return False
            
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role in ['buyer', 'seller']
        return False


class IsSellerOrAdmin(permissions.BasePermission):
    """
    Allows access to sellers and admins.
    """
    
    def has_permission(self, request, view):
        if not request.user or request.user == AnonymousUser():
            return False
            
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role in ['seller', 'admin']
        return False


class IsBuyerOrAdmin(permissions.BasePermission):
    """
    Allows access to buyers and admins.
    """
    
    def has_permission(self, request, view):
        if not request.user or request.user == AnonymousUser():
            return False
            
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role in ['buyer', 'admin']
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows access only to object owner or read-only access.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read access for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write access for object owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'buyer'):
            return obj.buyer == request.user or obj.seller == request.user
        elif hasattr(obj, 'seller'):
            return obj.seller == request.user
            
        return False


class IsSellerOrOwner(permissions.BasePermission):
    """
    Allows access to sellers or object owner.
    """
    
    def has_permission(self, request, view):
        if not request.user or request.user == AnonymousUser():
            return False
            
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role in ['seller', 'admin']
        return False
    
    def has_object_permission(self, request, view, obj):
        # Sellers can access their own objects
        if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'seller':
            if hasattr(obj, 'seller'):
                return obj.seller == request.user
            elif hasattr(obj, 'user'):
                return obj.user == request.user
                
        return False


def get_user_role(request):
    """
    Helper function to get user role from JWT token.
    """
    try:
        auth = JWTAuthentication().authenticate(request)
        if auth is not None:
            user, token = auth
            if hasattr(user, 'userprofile'):
                return user.userprofile.role
        return 'buyer'  # default role
    except (InvalidToken, AttributeError):
        return None
