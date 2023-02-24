from django.db import models
import datetime


class CommonCompanyInfo(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    address = models.CharField(null=True, blank=True, max_length=100)
    zip_code = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=True, max_length=100)
    state = models.CharField(null=True, blank=True, max_length=100)
    company_id_number = models.CharField(null=True, blank=True, max_length=100)
    bank_account_number = models.CharField(
        null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Company(CommonCompanyInfo):
    pass


class Client(CommonCompanyInfo):
    pass


class InvoiceSetting(models.Model):
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.CASCADE)
    discount = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True)
    # TODO currency =

    def __str__(self):
        return "Invoice settings"


class Invoice(models.Model):
    number = models.CharField(null=True, blank=True, max_length=100)
    date = models.DateField(null=True, blank=True)
    mailed = models.BooleanField(default=False)
    client = models.ForeignKey(
        Client, null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_products = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True)
    total_discount = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True)
    total_base = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True)
    total_tax = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True)
    invoice_settings = models.ForeignKey(
        InvoiceSetting, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

    @classmethod
    def get_invoice_number(self):
        try:
            last_invoice = Invoice.objects.latest('id')
        except Invoice.DoesNotExist:
            last_invoice = None

        today = datetime.date.today()
        year = today.year

        if last_invoice is None:
            new_invoice_number = "{}-{:04d}".format(year, 1)
        else:
            last_invoice = int(last_invoice.number.split("-")[1])
            new_invoice_number = "{}-{:04d}".format(year, last_invoice + 1)

        return new_invoice_number

    def save(self, *args, **kwargs):
        if self.number is None:
            self.number = self.get_invoice_number()
        self.company = Company.objects.get(id=1)
        self.invoice_settings = InvoiceSetting.objects.get(id=1)
        super(Invoice, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(
        max_digits=19, decimal_places=3, null=True, blank=True)
    price = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True)
    invoice = models.ForeignKey(
        Invoice, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DocumentPdf(models.Model):

    file_name = models.CharField(max_length=200)
    invoice = models.ForeignKey(
        Invoice, blank=True, null=True, on_delete=models.CASCADE)
    file_pdf = models.FileField(upload_to='invoices_pdf/')

    def __str__(self):
        return "hello"
