from django.urls import path

from . import views

urlpatterns = [
    path("print/ot/<int:pk>/", views.print_ot, name="print_ot"),
    path("print/ot/<int:pk>/duo/", views.print_ot_duo, name="print_ot_duo"),
    path("print/presupuesto/<int:pk>/", views.print_quote, name="print_quote"),
    path("print/factura/<int:pk>/", views.print_invoice, name="print_invoice"),
    path("pdf/ot/<int:pk>/", views.pdf_ot, name="pdf_ot"),
    path("pdf/ot/<int:pk>/duo/", views.pdf_ot_duo, name="pdf_ot_duo"),
    path("pdf/presupuesto/<int:pk>/", views.pdf_quote, name="pdf_quote"),
    path("pdf/factura/<int:pk>/", views.pdf_invoice, name="pdf_invoice"),
    # by number
    path("print/ot-numero/<str:numero>/", views.print_ot_by_num, name="print_ot_by_num"),
    path(
        "print/ot-numero/<str:numero>/duo/", views.print_ot_duo_by_num, name="print_ot_duo_by_num"
    ),
    path(
        "print/presupuesto-numero/<str:numero>/",
        views.print_quote_by_num,
        name="print_quote_by_num",
    ),
    path(
        "print/factura-numero/<str:numero>/",
        views.print_invoice_by_num,
        name="print_invoice_by_num",
    ),
    path("pdf/ot-numero/<str:numero>/", views.pdf_ot_by_num, name="pdf_ot_by_num"),
    path("pdf/ot-numero/<str:numero>/duo/", views.pdf_ot_duo_by_num, name="pdf_ot_duo_by_num"),
    path("pdf/presupuesto-numero/<str:numero>/", views.pdf_quote_by_num, name="pdf_quote_by_num"),
    path("pdf/factura-numero/<str:numero>/", views.pdf_invoice_by_num, name="pdf_invoice_by_num"),
]
