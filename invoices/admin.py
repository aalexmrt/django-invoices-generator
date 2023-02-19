from django.contrib import admin

# Register your models here.
from .models import Invoice, Client, Company, Product, DocumentPdf, InvoiceSetting

admin.site.register(Invoice)
admin.site.register(Client)
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(DocumentPdf)
admin.site.register(InvoiceSetting)
