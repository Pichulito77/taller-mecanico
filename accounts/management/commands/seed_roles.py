from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

BASE_ROLES = [
    "administrador",
    "recepcionista",
    "mecanico",
]


class Command(BaseCommand):
    help = "Create base roles (groups) if they do not exist"

    def handle(self, *args, **options):
        created = []
        for role in BASE_ROLES:
            group, was_created = Group.objects.get_or_create(name=role)
            if was_created:
                created.append(role)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created roles: {', '.join(created)}"))
        else:
            self.stdout.write("Roles already present; no changes.")