from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from workorders.models import WorkOrder, WorkOrderItem


class Command(BaseCommand):
    help = "Assign model permissions for WorkOrder and WorkOrderItem to default groups"

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name="administrador")
        recep_group, _ = Group.objects.get_or_create(name="recepcionista")
        mec_group, _ = Group.objects.get_or_create(name="mecanico")

        for model in (WorkOrder, WorkOrderItem):
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct)
            perm_map = {p.codename: p for p in perms}

            # Admin: todo
            admin_group.permissions.add(*perm_map.values())

            # Recepcionista: add/change/view (no delete por defecto)
            for codename in (f"add_{model._meta.model_name}", f"change_{model._meta.model_name}", f"view_{model._meta.model_name}"):
                if codename in perm_map:
                    recep_group.permissions.add(perm_map[codename])

            # Mecánico: view
            codename = f"view_{model._meta.model_name}"
            if codename in perm_map:
                mec_group.permissions.add(perm_map[codename])

        self.stdout.write(self.style.SUCCESS("Workorders permissions assigned to groups."))