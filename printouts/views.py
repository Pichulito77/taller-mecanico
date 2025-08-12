from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from workorders.models import WorkOrder
from billing.models import Quote, Invoice
from io import BytesIO


def render_to_pdf(template_name: str, context: dict) -> HttpResponse:
    # Lazy import to avoid import-time failures when reportlab/xhtml2pdf are missing from the environment
    from xhtml2pdf import pisa

    html = render(None, template_name, context).content.decode("utf-8")
    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse("Error generando PDF", status=500)
    resp = HttpResponse(result.getvalue(), content_type="application/pdf")
    return resp


def print_ot(request, pk: int):
    variant = request.GET.get("v", "empresa")
    ot = get_object_or_404(WorkOrder, pk=pk)
    return render(request, "printouts/ot_print.html", {"ot": ot, "variant": variant})


def print_ot_duo(request, pk: int):
    ot = get_object_or_404(WorkOrder, pk=pk)
    return render(request, "printouts/ot_print_duo.html", {"ot": ot})


def print_quote(request, pk: int):
    variant = request.GET.get("v", "empresa")
    qt = get_object_or_404(Quote, pk=pk)
    return render(request, "printouts/quote_print.html", {"quote": qt, "variant": variant})


def print_invoice(request, pk: int):
    variant = request.GET.get("v", "empresa")
    inv = get_object_or_404(Invoice, pk=pk)
    return render(request, "printouts/invoice_print.html", {"invoice": inv, "variant": variant})


def pdf_ot(request, pk: int):
    ot = get_object_or_404(WorkOrder, pk=pk)
    return render_to_pdf("printouts/ot_print.html", {"ot": ot, "variant": request.GET.get("v", "empresa")})


def pdf_ot_duo(request, pk: int):
    ot = get_object_or_404(WorkOrder, pk=pk)
    return render_to_pdf("printouts/ot_print_duo.html", {"ot": ot})


def pdf_quote(request, pk: int):
    qt = get_object_or_404(Quote, pk=pk)
    return render_to_pdf("printouts/quote_print.html", {"quote": qt, "variant": request.GET.get("v", "empresa")})


def pdf_invoice(request, pk: int):
    inv = get_object_or_404(Invoice, pk=pk)
    return render_to_pdf("printouts/invoice_print.html", {"invoice": inv, "variant": request.GET.get("v", "empresa")})