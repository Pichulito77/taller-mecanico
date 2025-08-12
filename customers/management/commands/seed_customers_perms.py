from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from customers.models import Cliente, Vehiculo


class Command(BaseCommand):
    help = "Assign model permissions for Cliente and Vehiculo to default groups"

    def handle(self, *args, **options):
        # Groups
        admin_group, _ = Group.objects.get_or_create(name="administrador")
        recep_group, _ = Group.objects.get_or_create(name="recepcionista")
        mec_group, _ = Group.objects.get_or_create(name="mecanico")

        for model in (Cliente, Vehiculo):
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct)
            perm_map = {p.codename: p for p in perms}

            # Admin: all perms
            admin_group.permissions.add(*perm_map.values())

            # Recepcionista: add, change, view
            for codename in (f"add_{model._meta.model_name}", f"change_{model._meta.model_name}", f"view_{model._meta.model_name}"):
                if codename in perm_map:
                    recep_group.permissions.add(perm_map[codename])

            # Mecánico: solo view
            codename = f"view_{model._meta.model_name}"
            if codename in perm_map:
                mec_group.permissions.add(perm_map[codename])

        self.stdout.write(self.style.SUCCESS("Customer permissions assigned to groups."))