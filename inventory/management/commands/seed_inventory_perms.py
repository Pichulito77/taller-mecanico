from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from inventory.models import InventoryMove, Part


class Command(BaseCommand):
    help = "Assign inventory permissions to default groups"

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name="administrador")
        recep_group, _ = Group.objects.get_or_create(name="recepcionista")
        mec_group, _ = Group.objects.get_or_create(name="mecanico")

        for model in (Part, InventoryMove):
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct)
            perm_map = {p.codename: p for p in perms}

            admin_group.permissions.add(*perm_map.values())

            for codename in (
                f"add_{model._meta.model_name}",
                f"change_{model._meta.model_name}",
                f"view_{model._meta.model_name}",
            ):
                if codename in perm_map:
                    recep_group.permissions.add(perm_map[codename])

            codename = f"view_{model._meta.model_name}"
            if codename in perm_map:
                mec_group.permissions.add(perm_map[codename])

        self.stdout.write(self.style.SUCCESS("Inventory permissions assigned to groups."))
