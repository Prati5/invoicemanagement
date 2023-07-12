from django.urls import path
from .views import InvoiceView

urlpatterns = [
    path('invoices', InvoiceView.as_view()),
    path('invoice/<str:pk>', InvoiceView.as_view()) # to capture our ids
]