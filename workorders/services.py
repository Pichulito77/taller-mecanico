from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from workorders.models import WorkOrder, WorkOrderItem
from inventory.models import Part, InventoryMove


@transaction.atomic
def finalize_workorder_and_deduct_inventory(ot: WorkOrder, user_id: int | None = None) -> None:
    # Validate state transition
    if not WorkOrder.is_valid_transition(ot.estado, "finalizada") and ot.estado != "finalizada":
        raise ValidationError("No se puede finalizar desde el estado actual")

    # Gather repuesto items
    items = WorkOrderItem.objects.filter(workorder=ot, tipo="repuesto")

    # Check stock availability
    parts_needed: dict[int, Decimal] = {}
    for it in items:
        if not it.repuesto_id:
            continue
        parts_needed[it.repuesto_id] = parts_needed.get(it.repuesto_id, Decimal("0")) + (it.cantidad or 0)

    parts = {p.id: p for p in Part.objects.filter(id__in=parts_needed.keys())}
    for repuesto_id, qty_needed in parts_needed.items():
        part = parts.get(repuesto_id)
        if part is None:
            raise ValidationError(f"Repuesto {repuesto_id} inexistente")
        if part.stock_actual < qty_needed:
            raise ValidationError(
                f"Stock insuficiente para repuesto {part.sku}: {part.stock_actual} < {qty_needed}"
            )

    # Deduct stock and create movements
    for it in items:
        if not it.repuesto_id:
            continue
        part = parts[it.repuesto_id]
        part.stock_actual = (part.stock_actual or 0) - (it.cantidad or 0)
        part.save(update_fields=["stock_actual", "updated_at"])  # unmanaged but writable
        InventoryMove.objects.create(
            repuesto=part,
            tipo="salida",
            cantidad=it.cantidad,
            costo_unitario=part.precio_lista,
            total_costo=(it.cantidad or 0) * (part.precio_lista or 0),
            referencia=f"OT {ot.numero}",
            ot_id=ot.id,
            user_id=user_id,
        )

    # Set state to finalizada if not already
    if ot.estado != "finalizada":
        ot.estado = "finalizada"
        ot.save(update_fields=["estado", "updated_at"])