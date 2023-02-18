from django.urls import path

from . import views

urlpatterns = [
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('create_build_invoice/<int:id>/',
         views.create_build_invoice, name='create_build_invoice'),
    path('invoice_pdf/<int:id>/', views.invoice_pdf, name='invoice_pdf'),
    path('', views.index, name='index'),
]
