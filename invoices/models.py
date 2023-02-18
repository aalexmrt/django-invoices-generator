from django.db import models
import datetime


class CommonCompanyInfo(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    address = models.CharField(null=True, blank=True, max_length=100)
    zip_code = models.IntegerField(null=True, blank=True)
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
        super(Invoice, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(null=True, blank=True)
    invoice = models.ForeignKey(
        Invoice, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DocumentPdf(models.Model):

    file_name = models.CharField(max_length=200)
    invoice = models.ForeignKey(
        Invoice, blank=True, null=True, on_delete=models.CASCADE)
    file_pdf = models.FileField(upload_to='invoices_pdf/')

    # @classmethod
    # def save_file(self, file_name):
    #     try:
    #         document = DocumentPDF.objects.filter(entry_document_pdf_contains="file_name")
    #     except: DocumentPDF.DoesNotExist:
    #         document = None
    #
    # def save(self, *args, **kwargs):
    #     if # OPTIMIZE:
    # print(document_pdf.name)
    # pdf_name = str(document_pdf).split("/")[1]

    # def __str__(self):
    #     return pdf_name
    # def __str__(self):
    #     return self.name
