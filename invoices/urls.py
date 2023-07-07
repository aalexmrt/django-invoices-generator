from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_invoice/', views.add_invoice, name='add_invoice'),
    path('check_pdf/<int:id>/', views.check_pdf, name='check_pdf'),
    path('delete_invoice/<int:id>/', views.delete_invoice, name='delete_invoice'),
    path('invoice_detail/<int:id>/', views.invoice_detail, name='invoice_detail'),
    path('make_customer/<int:id>/', views.make_customer, name='make_customer'),
    path('make_invoice/<int:id>/', views.make_invoice, name='make_invoice'),
    path('view_customers/', views.view_customers, name='view_customers'),
    path('view_invoices/', views.view_invoices, name='view_invoices'),
    path('', views.index, name='index'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
