from django.contrib import admin

from .models import Invoice, Client, Company, Product, DocumentPdf, InvoiceSetting, Contact

admin.site.register(Client)
admin.site.register(Company)
admin.site.register(DocumentPdf)
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(InvoiceSetting)
