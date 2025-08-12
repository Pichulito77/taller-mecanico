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
]