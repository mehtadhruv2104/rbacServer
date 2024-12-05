
from django.core.management.base import BaseCommand
from rbac_core.models import Permission

class Command(BaseCommand):
    help = 'Create initial permissions for the system'

    def handle(self, *args, **options):
        resources = [choice[0] for choice in Permission.RESOURCE_CHOICES]
        actions = [choice[0] for choice in Permission.ACTION_CHOICES]

        created_count = 0
        for resource in resources:
            for action in actions:
                permission, created = Permission.objects.get_or_create(
                    resource=resource,
                    action=action,
                    defaults={
                        'description': f"Permission to {action.lower()} {resource.lower()}"
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created permission: {resource} - {action}'))

        if created_count == 0:
            self.stdout.write(self.style.WARNING('No new permissions created. All permissions already exist.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} new permissions'))