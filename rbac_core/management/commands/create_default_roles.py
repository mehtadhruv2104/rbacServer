
from django.core.management.base import BaseCommand
from rbac_core.models import Permission,Role

class Command(BaseCommand):
    help = 'Create default roles'

    def handle(self, *args, **options):
        permissions = Permission.objects.all()
        read_permissions = permissions.filter(action='READ')
        admin_permission_ids = permissions.values_list('id', flat=True)
        Role.objects.create(id=1,name='ADMIN', permission_ids=list(admin_permission_ids))

        supervisor_permission_ids = permissions.exclude(action='DELETE').values_list('id', flat=True)
        Role.objects.create(id=2,name='SUPERVISOR', permission_ids=list(supervisor_permission_ids))

        staff_permission_ids = read_permissions.values_list('id', flat=True)
        Role.objects.create(id=3,name='STAFF', permission_ids=list(staff_permission_ids))

        

        