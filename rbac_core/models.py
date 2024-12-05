from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

class Permission(models.Model):

    id = models.AutoField(primary_key=True)
    
    RESOURCE_CHOICES = [
        ('CLUSTER', 'Cluster'),
        ('PIPELINES', 'Pipelines'),
        ('RELEASES', 'Releases'),
    
    ]
    
    ACTION_CHOICES = [
        ('READ', 'Read'),
        ('WRITE', 'Write'),
        ('DELETE', 'Delete'),
        ('UPDATE', 'Update'),
    ]
    
    resource = models.CharField(
        max_length=50, 
        choices=RESOURCE_CHOICES
    )
    action = models.CharField(
        max_length=50, 
        choices=ACTION_CHOICES
    )
    description = models.TextField(
        blank=True, 
        null=True
    )
    
    class Meta:
        unique_together = ('resource', 'action')
        indexes = [
            models.Index(fields=['resource', 'action']),
            models.Index(fields=['id'])
        ]
    
    def __str__(self):
        return f"{self.id}: {self.resource} - {self.action}"

class Role(models.Model):

    ROLE_CHOICES = [
        ('STAFF', 'Staff'),
        ('SUPERVISOR', 'Supervisor'),
        ('ADMIN', 'Admin'),
    ]

    id = models.AutoField(primary_key=True)
    
    name = models.CharField(
        max_length=50, 
        unique=True, 
        choices=ROLE_CHOICES
    )
    
    permission_ids = models.JSONField(
        default=list,
        blank=True
    )
    
    def __str__(self):
        return self.name
    
    def add_permission(self, permission):
        if permission.id not in self.permission_ids:
            self.permission_ids.append(str(permission.id))
            self.save()
    
    def remove_permission(self, permission):
        if str(permission.id) in self.permission_ids:
            self.permission_ids.remove(str(permission.id))
            self.save()
    
    def has_permission(self, resource, action):
        matching_permission = Permission.objects.filter(
            resource=resource, 
            action=action,
            id__in=[uuid.UUID(pid) for pid in self.permission_ids]
        ).first()
        
        return matching_permission is not None

class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('STAFF', 'Staff'),
        ('SUPERVISOR', 'Supervisor'),
        ('ADMIN', 'Admin'),
    ]

    role_name = models.CharField(
        max_length=50, 
        null=True,
        choices=ROLE_CHOICES
    )
    
    def __str__(self):
        return f"{self.username} - {self.role_id if self.role_id else 'No Role'}"
    

    

class AuditLog(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE
    )
    resource = models.CharField(max_length=50)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_allowed = models.BooleanField()
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        status = "Allowed" if self.is_allowed else "Denied"
        return f"{self.user.username} - {self.resource} {self.action} - {status}"