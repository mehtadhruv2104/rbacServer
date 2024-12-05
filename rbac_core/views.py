from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Role,Permission,CustomUser
from .serializers import UserSerializer,PermissionSerializer,RoleSerializer
from rest_framework import viewsets



class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            return Response({
                "success": True,
                "message": "User created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except serializers.ValidationError as e:
            return Response({
                "success": False,
                "message": str(e.detail),
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "success": True,
            "message": "Users retrieved successfully",
            "data": serializer.data
        })
    
    def partal_update(self, request, pk=None):
        try:
            try:
                user = CustomUser.objects.get(id=pk)
            except CustomUser.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "User not found"
                }, status=status.HTTP_404_NOT_FOUND)

 
            role_name = request.data.get('role_name')
            if not role_name:
                return Response({
                    "success": False,
                    "message": "Role name is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                role = Role.objects.get(name=role_name)
            except Role.DoesNotExist:
                return Response({
                    "success": False,
                    "message": f"Role '{role_name}' not found"
                }, status=status.HTTP_400_BAD_REQUEST)
      
            user.role_name = role.name
            user.save()

            return Response({
                "success": True,
                "message": f"Role '{role.name}' assigned successfully",
                "data": self.get_serializer(user).data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "An unexpected error occurred"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AssignRolesViewSet(viewsets.ModelViewSet): 
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    def partal_update(self, request, pk=None):
        try:
            try:
                user = CustomUser.objects.get(id=pk)
                print("user",user)
            except CustomUser.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "User not found"
                }, status=status.HTTP_404_NOT_FOUND)

 
            role_name = request.data.get('role_name')
            if not role_name:
                return Response({
                    "success": False,
                    "message": "Role name is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                role = Role.objects.get(name=role_name)
            except Role.DoesNotExist:
                return Response({
                    "success": False,
                    "message": f"Role '{role_name}' not found"
                }, status=status.HTTP_400_BAD_REQUEST)
      
            user.role = role
            user.save()

            return Response({
                "success": True,
                "message": f"Role '{role.name}' assigned successfully",
                "data": self.get_serializer(user).data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "An unexpected error occurred"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



class PermissionViewSet(viewsets.ReadOnlyModelViewSet):  # Read-only for GET requests
    queryset = Permission.objects.all()
    print(vars(queryset))
    serializer_class = PermissionSerializer

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "success": True,
            "message": "List of permissions retrieved successfully",
            "data": serializer.data
        })
    

class RolesViewSet(viewsets.ModelViewSet): 
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "success": True,
            "message": "List of Roles retrieved successfully",
            "data": serializer.data
        })


class SpecificRolesPermissionViewSet(viewsets.ModelViewSet): 
    
    def list(self, request, role_name=None):
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            return Response({
            "success": False,
            "message": "Bad Request. Incorrect Role Name",
        })
        permissionIds = role.permission_ids
        permissions = Permission.objects.filter(id__in=permissionIds)
        
        serializer = PermissionSerializer(permissions, many=True)
        return Response({
            "success": True,
            "message": "List of Roles retrieved successfully",
            "data": serializer.data
        })
    
    
    def update(self, request,pk, role_name=None):
        update_id = pk
        
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            return Response({
            "success": False,
            "message": "Bad Request. Incorrect Role Name",
            })
        new_permission_ids = request.data.get('permission_ids', [])
        if not new_permission_ids:
            return Response({
            "success": False,
            "message": "Bad Request. No permission ID's Given",
            })
        invalid_ids = [pid for pid in new_permission_ids if not Permission.objects.filter(id=pid).exists()]
        if invalid_ids:
            return Response({
            "success": False,
            "message": "Bad Request. Permission Id given is wrong"
            })

        role.permission_ids = new_permission_ids
        role.save()
        new_permissions = Permission.objects.filter(id__in=role.permission_ids)
        serializer = PermissionSerializer(new_permissions, many=True)
        
        return Response({
            "success": True,
            "message": "List of Roles retrieved successfully",
            "data": serializer.data
        })


class ValidateUserViewSet(viewsets.ModelViewSet): 
    
    def retrieve(self, request, pk=None):
        resource = request.query_params.get('resource')
        action = request.query_params.get('action')

        if not resource or not action:
            return Response({
            "success": False,
            "message": "Bad Request. Resource or Action not given",
            })

        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({
            "success": False,
            "message": "User not found",
            })

        has_permission = self.check_user_permission(user, resource, action)
        response = {
            "user_id": pk,
            "resource": resource,
            "action": action,
            "has_permission": has_permission
        }
        return Response({
            "success": True,
            "message": "Validation Successful",
            "data": response
        })
       
    
    def check_user_permission(self, user, resource, action):
        
        role_name = user.role_name
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            return Response({
            "success": False,
            "message": "Bad Request. Incorrect Role Name",
            })
        permission = Permission.objects.get(resource=resource, action=action)
        print(permission)
        print(role.permission_ids)
        if permission.id in role.permission_ids:
            access = True
        else :   
            access = False
        return access

    
    
  
