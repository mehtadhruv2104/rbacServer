# from django.urls import path
# from .views import RoleViewSet, UserViewSet, PermissionViewSet, AuditLogViewSet
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,PermissionViewSet,RolesViewSet,SpecificRolesPermissionViewSet,ValidateUserViewSet

urlpatterns = []
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'users/validate', ValidateUserViewSet, basename='user/validate')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'roles', RolesViewSet, basename='roles')
router.register(r'roles/permissions/(?P<role_name>\w+)', SpecificRolesPermissionViewSet, basename='roles/permissions')

urlpatterns += router.urls