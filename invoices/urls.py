from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('add_invoice/', views.add_invoice, name='add_invoice'),
    path('make_invoice/<int:id>/', views.make_invoice, name='make_invoice'),
    path('invoice_detail/<int:id>/', views.invoice_detail, name='invoice_detail'),
    path('send_email/<int:id>/', views.send_email, name='send_email'),
    path('check_pdf/<int:id>/', views.check_pdf, name='check_pdf'),
    path('', views.index, name='index'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
