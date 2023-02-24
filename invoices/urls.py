from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('create_build_invoice/<int:id>/',
         views.create_build_invoice, name='create_build_invoice'),
    path('invoice_detail/<int:id>/', views.invoice_detail, name='invoice_detail'),
    path('', views.index, name='index'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
